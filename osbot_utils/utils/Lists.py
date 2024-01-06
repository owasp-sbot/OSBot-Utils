import sys
from typing import List

from osbot_utils.utils.Objects import dict_insert_field, env_vars, list_set, obj_dict
from osbot_utils.utils.Str     import trim


#to do refactor out this class since it is not adding much value
class Lists:

    @staticmethod
    def chunks(list, split_by):
        n = max(1, split_by)
        return (list[i:i + n] for i in range(0, len(list), n))

    @staticmethod
    def delete(list, item):
        if item in list:
            list.remove(item)
        return list

    @staticmethod
    def first(list, strip=False):
        if Lists.not_empty(list):
            value = list[0]
            if strip:
                value = value.strip()
            return value

    @staticmethod
    def not_empty(list):
        if list and type(list).__name__ == 'list' and len(list) >0:
            return True
        return False

    @staticmethod
    def empty(list):
        return not Lists.not_empty(list)

    @staticmethod
    def lower(input_list):
        return [item.lower() for item in input_list]

    @staticmethod
    def tuple_to_list(target:tuple):
            if type(target) is tuple:
                return list(target)

    @staticmethod
    def tuple_replace_position(target:tuple, position,value):
        tuple_as_list = tuple_to_list(target)
        if len(tuple_as_list) > position:
            tuple_as_list[position] = value
        list_as_tuple = list_to_tuple(tuple_as_list)
        return list_as_tuple

    @staticmethod
    def list_to_tuple(target: list):
        if type(target) is list:
            return tuple(target)

    @staticmethod
    def list_dict_insert_field(target_list, new_key, insert_at, new_value=None):
        new_list = []
        for target_dict in target_list:
            kvwargs = dict(target_dict = target_dict,
                           new_key     = new_key    ,
                           insert_at   = insert_at  ,
                           new_value   = new_value  )
            new_dict = dict_insert_field(**kvwargs)
            new_list.append(new_dict)
        return new_list

def chunks(items:list, split: int):
    if items and split and split > 0:
        for i in range(0, len(items), split):
            yield items[i:i + split]

def len_list(target):
    return len(list(target))

def list_add(array : list, value):
    if value is not None:
        array.append(value)
    return value

def list_contains_list(array : list, values):
    if array is not None:
        if type(values) is list:
            for item in values:
                if (item in array) is False:
                    return False
            return True
    return False

def list_remove_list(source: list, target: list):
    if type(source) is list and type(target) is list:
        for item in target:
            if item in source:
                source.remove(item)

def list_find(array:list, item):
    if item in array:
        return array.index(item)
    return -1

def list_get_field(values, field):
    return [item.get(field) for item in values]

def list_index_by(values, index_by):
    from osbot_utils.fluent.Fluent_Dict import Fluent_Dict
    results = {}
    if values and index_by:
        for item in values:
            results[item.get(index_by)] = item
    return Fluent_Dict(results)

def list_group_by(values, group_by):
    results = {}
    for item in values:
        value = str(item.get(group_by))
        if results.get(value) is None: results[value] = []
        results[value].append(item)
    return results

def list_get(array, position=None, default=None):
    if type(array) is list:
        if type(position) is int and position >=0 :
            if  len(array) > position:
                return array[position]
    return default

def list_order_by(urls: List[dict], key: str, reverse: bool=False) -> List[dict]:
    """
    Sorts a list of dictionaries containing URLs by a specified key.

    Args:
        urls (List[dict]): A list of dictionaries containing URLs.
        key (str): The key to sort the URLs by.
        reverse (bool): Whether to sort the URLs in reverse order.

    Returns:
        List[dict]: The sorted list of URLs.
    """
    return sorted(urls, key=lambda x: x[key], reverse=reverse)

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

def list_set_dict(target):
    return sorted(list(set(obj_dict(target))))

def list_stats(target):
    stats = {}
    for item in target:
        if stats.get(item) is None:
            stats[item] = 0
        stats[item] += 1
    return stats

def list_remove(array, item):
    if type(item) is list:
        result = []
        for element in array:
            if element not in item:
                result.append(element)
        return result

    return [element for element in array if element != item]


def list_remove_empty(array):
    return [element for element in array if element]

def list_zip(*args):
    return list(zip(*args))

def list_filter(target_list, filter_function):
    return list(filter(filter_function, target_list))

def list_sorted(target_list, key, descending=False):
    return list(sorted(target_list, key= lambda x:x.get(key,None) ,reverse=descending))

def list_filter_starts_with(target_list, prefix):
    return list_filter(target_list, lambda x: x.startswith(prefix))

def list_filter_contains(target_list, value):
    return list_filter(target_list, lambda x: x.find(value) > -1)

def env_vars_list():
    return list_set(env_vars())

def unique(target):
    return list_set(target)

def sys_path_python(python_folder='lib/python'):
    return list_contains(sys.path, python_folder)


array_find             = list_find
array_get              = list_get
array_pop              = list_pop
array_pop_and_trim     = list_pop_and_trim
array_add              = list_add

list_contains          = list_filter_contains
list_chunks            = Lists.chunks
list_dict_insert_field = Lists.list_dict_insert_field       # todo: see if I can move this ot the objects class
list_del               = Lists.delete
list_empty             = Lists.empty
list_first             = Lists.first
list_lower             = Lists.lower
list_not_empty         = Lists.not_empty
list_sort_by           = list_sorted
list_to_tuple          = Lists.list_to_tuple

tuple_to_list          = Lists.tuple_to_list
tuple_replace_position = Lists.tuple_replace_position
