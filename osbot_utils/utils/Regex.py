import re

from osbot_utils.utils.Status import status_error


def list__match_regex(target, pattern):
    return list__match_regexes(target, [pattern])

def list__match_regexes(target, *patterns):
    if len (patterns) == 0:
        return target
    compiled_patterns = []
    for pattern in patterns:
        try:
            compiled_patterns.append(re.compile(pattern))                           # todo: find better way to handle regex errors
        except Exception as error:
            return status_error(message='Error compiling pattern: {pattern}', error=error)
    matched_files = []
    if target and type(target) is list:
        for file in target:
            for compiled_pattern in compiled_patterns:
                if compiled_pattern.match(file):
                    matched_files.append(file)
                    break
    return matched_files