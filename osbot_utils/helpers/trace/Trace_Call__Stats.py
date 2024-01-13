from collections import defaultdict, Counter
from copy import copy

from osbot_utils.utils.Dev import pprint

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class Trace_Call__Stats(Kwargs_To_Self):

    calls          : int
    calls_skipped  : int
    exceptions     : int
    lines          : int
    returns        : int
    unknowns       : int            # to use for extra events that are not being captured
    raw_call_stats : list

    def __repr__(self):
        return str(self.stats())

    def __eq__(self, target):
        if self is target:
            return True
        return self.stats() == target

    def log_frame(self, frame):
        code        = frame.f_code
        func_name   = code.co_name
        module      = frame.f_globals.get("__name__", "")
        self.raw_call_stats.append((module, func_name))
        return self

    def frames_stats__build_tree(self, d, path, function_name):
        parts = path.split('.')
        current_level = d
        for part in parts[:-1]:  # Go up to the second-to-last element
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        if parts[-1] not in current_level:
            current_level[parts[-1]] = Counter()
        current_level[parts[-1]][function_name] += 1

    def frames_stats(self):
        processed_frame_stats = self.frames_stats__process_raw_data()
        return self.to_standard_dict(processed_frame_stats)

    def frames_stats__process_raw_data(self):
        tree = defaultdict(dict)
        for module, function_name in self.raw_call_stats:
            self.frames_stats__build_tree(tree, module, function_name)
        return tree


    def to_standard_dict(self, d):
        if isinstance(d, defaultdict):
            d = {k: self.to_standard_dict(v) for k, v in d.items()}
        if isinstance(d, Counter):
            d = dict(d)
        if isinstance(d, dict):
            return {k: self.to_standard_dict(v) for k, v in d.items()}
        return d

    def stats(self):
        stats = copy(self.__locals__())
        del stats['raw_call_stats']
        return stats

    def print(self):
        pprint(self.stats())
