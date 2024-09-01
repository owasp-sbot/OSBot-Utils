import sys
from typing import List

from osbot_utils.utils.Misc import list_set

from osbot_utils.utils.Str     import trim

def len_list(target):
    if type(target) is list:
        return len(list(target))
    return 0

def list_add(array : list, value):
    if value is not None:
        array.append(value)
    return value

def list_chunks(items:list, split: int):
    if items and split and split > 0:
        for i in range(0, len(items), split):
            yield items[i:i + split]

def list_contains_list(array : list, values):
    if array is not None:
        if type(values) is list:
            for item in values:
                if (item in array) is False:
                    return False
            return True
    return False

def list_delete(target, item):
    if item in target:
        target.remove(item)
    return target

def list_empty(list):
    return not list_not_empty(list)

def list_filter(target_list, filter_function):
    return list(filter(filter_function, target_list))

def list_filter_starts_with(target_list, prefix):
    return list_filter(target_list, lambda x: x.startswith(prefix))

def list_filter_contains(target_list, value):
    return list_filter(target_list, lambda x: x.find(value) > -1)

def list_find(array:list, item):
    if item in array:
        return array.index(item)
    return -1

def list_first(list, strip=False):
    if list_not_empty(list):
        value = list[0]
        if strip:
            value = value.strip()
        return value

def list_in_list(source : list, target: list):
    return set(source).issubset(set(target))

def list_get(array, position=None, default=None):
    if type(array) is list:
        if type(position) is int and position >=0 :
            if  len(array) > position:
                return array[position]
    return default

def list_get_field(values, field):
    if type(values) is list:
        return [item.get(field) for item in values]
    return []

def list_group_by(values, group_by):
    results = {}
    if type(values) is list:
        for item in values:
            value = str(item.get(group_by))
            if results.get(value) is None: results[value] = []
            results[value].append(item)
    return results

def list_index_by(values, index_by):
    from osbot_utils.fluent.Fluent_Dict import Fluent_Dict
    results = {}
    if values and index_by:
        for item in values:
            results[item.get(index_by)] = item
    return Fluent_Dict(results)

def list_lower(input_list):
    return [item.lower() for item in input_list]

def list_minus_list(list_a, list_b):
    return [item for item in list_a if item not in list_b]

def list_not_empty(list):
    if list and type(list).__name__ == 'list' and len(list) >0:
        return True
    return False

def list_order_by(target: List[dict], key: str, reverse: bool=False) -> List[dict]:
    if target and key:
        return sorted(target, key=lambda x: x[key], reverse=reverse)
    return []

def list_pop(array:list, position=None, default=None):
    if array:
        if len(array) >0:
            if type(position) is int:
                if len(array) > position:
                    return array.pop(position)
            else:
                return array.pop()
    return default

def list_pop_and_trim(array, position=None):
    value = array_pop(array,position)
    if type(value) is str:
        return trim(value)
    return value

def list_remove(array, item):
    if type(array) is list:
        if type(item) is list:
            result = []
            for element in array:
                if element not in item:
                    result.append(element)
            return result

        return [element for element in array if element != item]
    return array

def list_remove_list(source: list, target: list):
    if type(source) is list and type(target) is list:
        for item in target:
            if item in source:
                source.remove(item)
    return source

def list_remove_empty(array):
    if type(array) is list:
        return [element for element in array if element]
    return array

def list_set_dict(target):
    if hasattr(target, '__dict__'):
        return sorted(list(set(target.__dict__)))
    return []

def list_sorted(target_list, key, descending=False):
    return list(sorted(target_list, key= lambda x:x.get(key,None) ,reverse=descending))

def list_stats(target):
    stats = {}
    if type(target) is list:
        for item in target:
            if stats.get(item) is None:
                stats[item] = 0
            stats[item] += 1
    return stats

def list_to_tuple(target: list):
    if type(target) is list:
        return tuple(target)

def list_zip(*args):
    if args:
        return list(zip(*args))

def sys_path_python(python_folder='lib/python'):
    return list_contains(sys.path, python_folder)

def tuple_to_list(target:tuple):
    if type(target) is tuple:
        return list(target)

def tuple_replace_position(target:tuple, position,value):
    tuple_as_list = tuple_to_list(target)
    if len(tuple_as_list) > position:
        tuple_as_list[position] = value
    list_as_tuple = list_to_tuple(tuple_as_list)
    return list_as_tuple

def unique(target):
    return list_set(target)

array_find             = list_find
array_get              = list_get
array_pop              = list_pop
array_pop_and_trim     = list_pop_and_trim
array_add              = list_add

list_contains          = list_filter_contains
list_del               = list_delete
list_sort_by           = list_sorted

chunks                 = list_chunks