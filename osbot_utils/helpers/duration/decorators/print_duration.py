from osbot_utils.helpers.duration.decorators.capture_duration import capture_duration


class print_duration(capture_duration):

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = super().__exit__(exc_type, exc_val, exc_tb)
        self.print()
        return result