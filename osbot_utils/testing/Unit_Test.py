import base64
from   unittest              import TestCase
from   osbot_utils.utils.Dev import pprint


class Unit_Test(TestCase):
    """Unit test helpers

        - self.result will be written to the output
        - self.png_data will be saved to '/tmp/unit-test.png'"""

    def setUp(self):
        self.png_file = '/tmp/unit-test.png'
        self.result   = None
        self.png_data = None

    def tearDown(self):
        if self.result is not None:
            pprint(self.result)
        if self.png_data is not None:
            if type(self.png_data) is bytes:
                with open(self.png_file, "wb") as file:
                    file.write(self.png_data)
                pprint(f'Png data with size {len(self.png_data)} saved to {self.png_file}')
            elif type(self.png_data) is str:
                try:
                    with open(self.png_file, "wb") as file:
                        file.write(base64.decodebytes(self.png_data.encode()))
                    pprint(f'Png data with size {len(self.png_data)} saved to {self.png_file}')
                except Exception as error:
                    pprint(f'png save error: {error}')
                    pprint(self.png_data)
            else:
                pprint(f'Error Png data was not a string: {self.png_data}')
