from typing                                                  import Dict
from osbot_utils.helpers.duration.Duration                   import Duration
from osbot_utils.helpers.flows.schemas.Schema__Flow__Status  import Schema__Flow__Status
from osbot_utils.helpers.flows.schemas.Schema__Task__Stats   import Schema__Task__Stats
from osbot_utils.helpers.flows.schemas.Schema__Flow__Stats   import Schema__Flow__Stats
from osbot_utils.type_safe.Type_Safe                         import Type_Safe

FLOW__ERROR_MESSAGE__TASK_FAILED = 'At least one task failed'

class Flow__Stats__Collector(Type_Safe):
    duration               : Duration
    stats                  : Schema__Flow__Stats
    task_execution_counter : int

    def start(self, flow_id: str, flow_name:str):
        self.duration.print_result = False
        self.duration.start()
        self.task_execution_counter = 0
        with self.stats as _:
            _.flow_id      = flow_id
            _.flow_name    = flow_name
            _.status       = Schema__Flow__Status.RUNNING
        return self

    def end(self, flow_error:Exception):
        self.duration.end()
        with self.stats as _:
            _.duration     = self.duration.data()
            _.total_tasks  = len(self.stats.tasks_stats)
            _.failed_tasks = sum(1 for task in self.stats.tasks_stats.values() if task.status == Schema__Flow__Status.FAILED)

            if flow_error:
                _.status = Schema__Flow__Status.FAILED
                _.error_message = str(flow_error)
            elif _.failed_tasks:
                _.status = Schema__Flow__Status.FAILED
                _.error_message = FLOW__ERROR_MESSAGE__TASK_FAILED
            else:
                _.status = Schema__Flow__Status.COMPLETED
        return self

    def get_next_execution_order(self):                                                                                 # Get the next execution order number and increment the counter."""
        self.task_execution_counter += 1
        return self.task_execution_counter

    def add_task_stats(self, task_stats: Schema__Task__Stats):                                                          # Add task stats to the collection.
        self.stats.tasks_stats[task_stats.task_id] = task_stats
        return self

    def json(self):                                                                                                     # Return JSON representation of the stats.
        return self.stats.json()

    def durations__with_tasks_status(self):
        with self.stats as _:
            tasks_durations = dict()
            flow_durations  = dict(flow_name     = _.flow_name                ,
                                   flow_duration = _.duration.duration_seconds,
                                   flow_status   = _.status.value             ,
                                   flow_tasks    =  tasks_durations           )

            for task_id, flow_task in self.stats.tasks_stats.items():
                task_duration   = dict(task_name = flow_task.task_name                     ,
                                       task_duration  = flow_task.duration.duration_seconds,
                                       task_status    = flow_task.status.value             )
                execution_order = flow_task.execution_order
                tasks_durations[execution_order] = task_duration
        return flow_durations

    def durations(self):
        with self.stats as _:
            if _.status is None:
                flow_durations = dict()
            else:
                tasks_durations = dict()
                flow_durations  = dict(flow_name     = _.flow_name                ,
                                       flow_duration = _.duration.duration_seconds,
                                       flow_status   = _.status.value             ,
                                       flow_tasks    =  tasks_durations           )

                for task_id, flow_task in self.stats.tasks_stats.items():

                    tasks_durations[flow_task.task_name] = flow_task.duration.duration_seconds
        return flow_durations