from typing                                                                         import Optional, Dict, Any
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now    import Timestamp_Now
from osbot_utils.helpers.flows.models.Flow_Run__Event                               import Flow_Run__Event
from osbot_utils.helpers.flows.models.Schema__Flow__Artifact                        import Schema__Flow__Artifact
from osbot_utils.helpers.flows.models.Schema__Flow__Result                          import Schema__Flow__Result
from osbot_utils.helpers.flows.schemas.Schema__Flow                                 import Schema__Flow
from osbot_utils.helpers.flows.schemas.Schema__Flow__Data                           import Schema__Flow__Data
from osbot_utils.helpers.flows.schemas.Schema__Flow__Log                            import Schema__Flow__Log
from osbot_utils.helpers.flows.schemas.Schema__Flow__Task__Data                     import Schema__Flow__Task__Data
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe


class Flow__Data(Type_Safe):
    flow_data : Schema__Flow__Data                                               # Main data container for flow execution

    def set_completed(self):                                                     # Mark flow as completed
        self.flow_data.end_time = Timestamp_Now()
        self.flow_data.status   = "completed"

    def set_error(self, error: Exception):                                      # Record flow execution error
        self.flow_data.end_time = Timestamp_Now()
        self.flow_data.status   = "failed"
        self.flow_data.error    = str(error)

    def set_flow_id(self, flow_id: str):                                        # Set flow identifier
        self.flow_data.flow_id = flow_id

    def set_flow_name(self, flow_name: str):                                    # Set flow name
        self.flow_data.flow_name = flow_name

    def set_return_value(self, value: Any):                                     # Set flow return value
        self.flow_data.return_value = value

    def add_task(self, task_id: str, task_name: str):                          # Record start of task execution
        self.flow_data.tasks[task_id] = Schema__Flow__Task__Data(task_id      = task_id         ,
                                                                 task_name    = task_name       ,
                                                                 start_time   = Timestamp_Now() ,
                                                                 end_time     = None            ,
                                                                 status       = ""              ,
                                                                 error_message= None            ,
                                                                 return_value = None            ,
                                                                 input_args   = ()              ,
                                                                 input_kwargs = {}              )

    def update_task(self, task_id: str, status: str,                            # Update task execution status
                    error: Optional[Exception] = None,
                    return_value: Any = None):
        if task_id in self.flow_data.tasks:
            task_data = self.flow_data.tasks[task_id]
            task_data.end_time      = Timestamp_Now()
            task_data.status        = status
            task_data.error_message = str(error) if error else None
            task_data.return_value  = return_value

    # def add_event(self, event: Schema__Flow__Event):                          # todo: this needs refactoring with the Flow_Run__Event events used below
    def add_event(self, event: Flow_Run__Event):                                # Record flow execution event
         self.flow_data.events.append(event)

    def add_log(self, level: int, message: str,                                 # Record log message
                task_id: Optional[str] = None):
        self.flow_data.logs.append(Schema__Flow__Log(
            timestamp = Timestamp_Now(),
            level     = level,
            message   = message,
            task_id   = task_id))

    def add_result(self, key: str, description: str):                           # Record flow execution result
        self.flow_data.results.append(Schema__Flow__Result(
            key         = key,
            description = description,
            timestamp   = Timestamp_Now()))

    def add_artifact(self, key          : str,
                           description  : str,
                           data         : Any,
                           artifact_type: str):                             # Record flow execution artifact

        self.flow_data.artifacts.append(Schema__Flow__Artifact(
            key         = key,
            description = description,
            data        = data,
            type        = artifact_type,
            timestamp   = Timestamp_Now()))

    def json(self) -> Dict[str, Any]:                                          # Convert flow data to JSON
        return Schema__Flow(flow_data=self.flow_data).json()