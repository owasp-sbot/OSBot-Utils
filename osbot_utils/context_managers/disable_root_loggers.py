import logging

class disable_root_loggers():
    def __init__(self):
        self.original_root_loggers  = []


    def __enter__(self):

        self.capture_root_loggers()                                         # capture current loggers
        logging.root.handlers.clear()                                       # removes all loggers
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.restore_root_loggers()                                         # restores original loggers
        return False                                                        # ensures that any exceptions that happened are rethrown

    def capture_root_loggers(self):
        for logger in logging.root.handlers:
            self.original_root_loggers.append(logger)
        return self

    def restore_root_loggers(self):
        for logger in self.original_root_loggers:
            logging.root.handlers.append(logger)
        return self
