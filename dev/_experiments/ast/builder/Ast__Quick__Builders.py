from typing import List, Dict

from osbot_utils.helpers.ast.builder.Ast__Python__Builder import Ast__Python__Builder


class QuickBuilders:
    """High-level builders for common patterns"""

    @staticmethod
    def data_class(name: str, fields: List[str], **options) -> Ast__Python__Builder:
        """Create a simple data class"""
        builder = Ast__Python__Builder()

        if options.get('use_dataclass', True):
            builder.add_from_import('dataclasses', ['dataclass'])

        class_builder = builder.add_class(name)

        if options.get('use_dataclass', True):
            class_builder.dataclass()

        # Add type hints if provided
        if 'field_types' in options:
            typed_fields = [f"{field}: {options['field_types'].get(field, 'Any')}"
                          for field in fields]
            class_builder.add_simple_init(typed_fields)
        else:
            class_builder.add_simple_init(fields)

        # Add common methods
        if options.get('add_str', True):
            class_builder.add_method('__str__').returns_string_concat(
                [f'"{name}("']
                + [part for field in fields for part in (f'", {field}="', f'self.{field}')]
                + ['")"']
            ).end_method()

        if options.get('add_repr', True):
            class_builder.add_method('__repr__').returns_call('str', ['self']).end_method()

        return class_builder.end_class()

    @staticmethod
    def crud_class(name: str, fields: List[str], table_name: str = None) -> Ast__Python__Builder:
        """Create a CRUD class"""
        table_name = table_name or name.lower() + 's'

        return (Ast__Python__Builder()
            .add_class(name)
                .add_init(['db_connection'])
                    .assign('self.db', 'db_connection')
                    .assign('self.table', f'"{table_name}"')
                .end_method()
                .add_method('create', fields)
                    .assign('record', '{' + ', '.join(f'"{f}": {f}' for f in fields) + '}')
                    .returns_call('self.db.insert', ['self.table', 'record'])
                .end_method()
                .add_method('read', ['id'])
                    .returns_call('self.db.select', ['self.table', 'id'])
                .end_method()
                .add_method('update', ['id', '**kwargs'])
                    .returns_call('self.db.update', ['self.table', 'id', 'kwargs'])
                .end_method()
                .add_method('delete', ['id'])
                    .returns_call('self.db.delete', ['self.table', 'id'])
                .end_method()
            .end_class())

    @staticmethod
    def api_client(name: str, base_url: str, endpoints: List[Dict]) -> Ast__Python__Builder:
        """Create an API client class"""
        builder = (Ast__Python__Builder()
            .add_import('requests')
            .add_class(name)
                .add_init(['token: str = None'])
                    .assign('self.base_url', f'"{base_url}"')
                    .assign('self.headers', '{}')
                    .add_if('token')
                        .assign('self.headers["Authorization"]', 'f"Bearer {token}"')
                    .end_if()
                .end_method())

        class_builder = builder._context_stack[-1]  # Get current class builder

        for endpoint in endpoints:
            method_name = endpoint['name']
            http_method = endpoint['method'].upper()
            path = endpoint['path']

            if http_method == 'GET':
                (class_builder
                    .add_method(method_name, ['**params'])
                        .assign('url', f'f"{{{base_url}}}{path}"')
                        .returns_call('requests.get', ['url'], {'headers': 'self.headers', 'params': 'params'})
                    .end_method())
            elif http_method == 'POST':
                (class_builder
                    .add_method(method_name, ['data'])
                        .assign('url', f'f"{{{base_url}}}{path}"')
                        .returns_call('requests.post', ['url'], {'headers': 'self.headers', 'json': 'data'})
                    .end_method())

        return class_builder.end_class()