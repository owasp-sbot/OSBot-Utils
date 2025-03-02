from osbot_utils.helpers.duration.Duration                  import Duration
from osbot_utils.helpers.flows.schemas.Schema__Flow__Status import Schema__Flow__Status
from osbot_utils.helpers.flows.schemas.Schema__Task__Stats  import Schema__Task__Stats
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

class Task__Stats__Collector(Type_Safe):
    duration       : Duration
    stats          : Schema__Task__Stats

    def start(self, flow_id: str, task_id: str, task_name: str , execution_order:int):
        self.duration.print_result = False
        self.duration.start()
        with self.stats as _:
            _.parent_flow_id  = flow_id
            _.execution_order = execution_order
            _.status          = Schema__Flow__Status.RUNNING
            _.task_id         = task_id
            _.task_name       = task_name
        return self

    def end(self, task_error: Exception):
        self.duration.end()
        with self.stats as _:
            _.duration = self.duration.data()
            if task_error:
                _.status        = Schema__Flow__Status.FAILED
                _.error_message = str(task_error)
            else:
                _.status = Schema__Flow__Status.COMPLETED
        return self


    def json(self):                                                                                                     # Return JSON representation of the stats.
        return self.stats.json()