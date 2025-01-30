from unittest                                           import TestCase
from osbot_utils.helpers.flows.models.Flow_Run__Config  import Flow_Run__Config


class test_Flow_Run__Config(TestCase):

    def setUp(self):
        self.config = Flow_Run__Config()

    def test_default_values(self):
        assert self.config.add_task_to_self         is True
        assert self.config.log_to_console           is False
        assert self.config.log_to_memory            is True
        assert self.config.logging_enabled          is True
        assert self.config.print_logs               is False
        assert self.config.print_none_return_value  is False
        assert self.config.print_finished_message   is False
        assert self.config.raise_flow_error         is True

    def test_custom_configuration(self):
        custom_config = Flow_Run__Config(
            add_task_to_self=False,
            log_to_console=True,
            log_to_memory=False,
            logging_enabled=False,
            print_logs=True,
            print_none_return_value=True,
            print_finished_message=True,
            raise_flow_error=False
        )

        assert custom_config.add_task_to_self is False
        assert custom_config.log_to_console is True
        assert custom_config.log_to_memory is False
        assert custom_config.logging_enabled is False
        assert custom_config.print_logs is True
        assert custom_config.print_none_return_value is True
        assert custom_config.print_finished_message is True
        assert custom_config.raise_flow_error is False

    def test_partial_configuration(self):
        partial_config = Flow_Run__Config(
            log_to_console=True,
            print_logs=True
        )

        # Modified values
        assert partial_config.log_to_console is True
        assert partial_config.print_logs is True

        # Default values
        assert partial_config.add_task_to_self is True
        assert partial_config.log_to_memory is True
        assert partial_config.logging_enabled is True
        assert partial_config.print_none_return_value is False
        assert partial_config.print_finished_message is False
        assert partial_config.raise_flow_error is True