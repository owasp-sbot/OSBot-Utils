from osbot_utils.base_classes.Type_Safe import Type_Safe


class Cache__Requests__Table(Type_Safe):

    def _table_create(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def row_add_and_commit(self, row_obj=None):
        raise NotImplementedError

    def rows_delete_where(self, **query_conditions):
        raise NotImplementedError
