from osbot_utils.helpers.trace.Trace_Call import Trace_Call


class Trace_Files(Trace_Call):

    files: list

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # def trace_calls(self, frame, event, arg):
    #     if event == 'call':
    #         self.files.append(frame.f_code.co_filename)
    #
    #     # if event != 'call':
    #     #     return
    #     #
    #     #
    #     #     # Get the function object being called
    #     # func = frame.f_globals.get(frame.f_code.co_name, None)
    #     #
    #     # # Retrieve the source code if the function object is available
    #     # if func:
    #     #     try:
    #     #         source_code = inspect.getsource(func)
    #     #         print(f"Source code of {func.__name__}:\n{source_code}\n")
    #     #     except TypeError:
    #     #         pass  # Handle cases where source code can't be retrieved
    #     #
    #
    #     return super().trace_calls(frame, event, arg)


