from osbot_utils.utils.Lists import list_sorted
from osbot_utils.base_classes.Kwargs_To_Self            import Kwargs_To_Self
from osbot_utils.helpers.trace.Trace_Call__Config       import Trace_Call__Config
from osbot_utils.helpers.trace.Trace_Call__Print_Traces import text_grey, text_bold_green, text_olive, text_light_grey
from osbot_utils.utils.Str import ansi_text_visible_length


class Trace_Call__Print_Lines(Kwargs_To_Self):

    config     : Trace_Call__Config
    view_model : list

    def lines(self):
        lines = []
        for trace in self.view_model:
            items          = trace.get('lines')
            leading_spaces = 0
            if items:
                line = items[0].get('line')
                leading_spaces = len(line) - len(line.lstrip())

            for line_data in items:
                depth_padding = '  ' + ' ' * (line_data.get('stack_size') - 2) * 6                      # this helps to align the code with the current depth (i.e. column alignment of code)
                line_data['line'] = depth_padding + line_data.get('line')[leading_spaces:]
                lines.append(line_data)
        return list_sorted(lines, 'index')

    def max_fields_length(self, items, *fields):
        max_length = 0
        for item in items:
            method_sig = '.'.join(str(item.get(field, '')) for field in fields)
            if len(method_sig) > max_length:
                max_length = len(method_sig)
        return max_length

    def max_fields_value(self, items, *fields):
        max_value = 0
        for item in items:
            values = [int(item.get(field, 0)) for field in fields if field in item and isinstance(item.get(field), int)]        # This will create a list of integers for the given fields in the line
            line_max = max(values) if values else 0                                                                             # Now find the max value from these integers
            if line_max > max_value:
                max_value = line_max
        return max_value

    def print_lines(self, ):
        lines = self.lines()
        print("--------- CALL TRACER (Lines)----------")
        print(f"Here are the {len(lines)} lines captured\n")

        max_length__sig  = self.max_fields_length(lines, 'module', 'func_name') + 2
        max_length__line = self.max_fields_length(lines, 'line'        ) + self.max_fields_value (lines, 'stack_size'  ) + 5                  # this +  5 helps with the alignment of the larger line (so that it doesn't overflow the table)
        max_length__self = self.max_fields_length(lines, 'self_local'  )
        print( '┌─────┬──────┬─' + '─' * max_length__line       +'──┬─' + '─' * max_length__sig                + '─┬─' + '─' * max_length__self      + '─┬───────┐   ')
        print(f"│ #   │ Line │ {'Source code':<{max_length__line}}  │ {'Method Class and Name':<{max_length__sig}} │ {'Self object':<{max_length__self}} │ Depth │   ")
        print( '├─────┼──────┼─' + '─' * max_length__line       +'──┼─' + '─'* max_length__sig                 + '─┼─'  + '─' * max_length__self     + '─┼───────┤   ')
        for line_data in lines:
            index       = line_data.get('index')
            func_name   = line_data.get('func_name')
            line_number = line_data.get('line_number')
            module      = line_data.get('module')
            event       = line_data.get('event')
            line        = line_data.get('line')
            self_local  = line_data.get('self_local') or ''
            method_sig  = f"{module}.{func_name}"
            stack_size  = line_data.get('stack_size') -1

            text_depth         = f'{stack_size:5}'
            text_depth_padding = ' ' * ((stack_size-1)  * 2)
            text_index         = f'{text_grey(index):12}'
            text_line_no       = f'{line_number:4}'
            text_method_sig    = f'{method_sig:{max_length__sig}}'

            if event == 'call':
                text_line = f'{text_bold_green(line)}'
            else:
                text_line = f'{text_light_grey(line)}'

            text_line_padding  =  ' ' * (max_length__line - ansi_text_visible_length(text_line) - len(text_depth_padding))
            text_source_code   = f'{text_depth_padding}{text_line} {text_line_padding}'

            print(f"│ {text_index} │ {text_line_no} │ {text_source_code} │ {text_method_sig} │ {self_local:<{max_length__self}} │ {text_depth} │")

        print('└─────┴──────┴──' + '─' * max_length__line + '─┴─' + '─' * max_length__sig + '─┴──'  + '─' * max_length__self + '┴───────┘')


