
class Dev:
    @staticmethod
    def jformat(data):
        import json

        return json.dumps(data, indent=4)       # use json.dumps to format

    @staticmethod
    def jprint(data):
        import json

        print()                                 # add a line before
        print(json.dumps(data, indent=4))       # use json.dumps to format
        return data

    @staticmethod
    def pformat(data):
        import pprint as original_pprint

        return original_pprint.pformat(data, indent=2)  # use a pprint to format

    @staticmethod
    def pprint(*args):
        import pprint as original_pprint

        print()                                # add a line before
        for arg in args:
            original_pprint.pprint(arg, indent=2)       # use a pprint to format
        if len(args) == 1:
            return args[0]
        return args

    @staticmethod
    def nprint(data):
        print()                                # add a line before
        print(data)
        return data

    @staticmethod
    def print_now():
        from osbot_utils.utils.Misc import date_time_now

        print(date_time_now())

jformat   = Dev.jformat
jprint    = Dev.jprint
pformat   = Dev.pformat
pprint    = Dev.pprint
nprint    = Dev.nprint

print_now = Dev.print_now