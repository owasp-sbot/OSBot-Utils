import sys
import traceback

from osbot_utils.utils.Objects import obj_data

def call_stack_current_frame():
    return sys._getframe()

def call_stack_format_stack(depth=None):
    return traceback.format_stack(limit=depth)

def call_stack_frames(depth=None):
    return traceback.extract_stack(limit=depth)

def call_stack_frames_data(depth=None):
    frames_data = []
    for frame in call_stack_frames(depth=depth):
        frames_data.append(obj_data(frame))
    return frames_data


