# special file use by pytest

# "%(asctime)s %(levelname)s %(name)s:%(filename)s:%(lineno)d %(message)s"
# "%(asctime)s %(levelname)s %(message)s"
LOG_FORMAT  = "%(asctime)s %(levelname)s %(filename)-20s %(message)s"
DATE_FORMAT = '%M:%S'
def pytest_configure(config):
    config.option.log_cli             = True                                         # Set log_cli to True to enable real-time logging output to the console
    config.option.log_cli_level       = 'DEBUG'                                      # Set the logging level (DEBUG, INFO, WARNING, etc.)
    config.option.log_format          = LOG_FORMAT                                   # Apply the logging format
    config.option.log_cli_date_format = DATE_FORMAT

