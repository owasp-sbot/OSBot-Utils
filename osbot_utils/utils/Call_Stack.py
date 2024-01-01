import sys
import traceback

from osbot_utils.utils.Objects import obj_data


class Call_Stack:

    def current_frame(self):
        return sys._getframe()

    def format_stack(self, depth=None):
        return traceback.format_stack(limit=depth)

    def frames(self, depth=None):
        return traceback.extract_stack(limit=depth)

    def frames_data(self, depth=None):
        frames_data = []
        for frame in self.frames(depth=depth):
            frames_data.append(obj_data(frame))
        return frames_data

