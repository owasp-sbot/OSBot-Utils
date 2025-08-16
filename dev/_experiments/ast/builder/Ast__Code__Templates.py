from osbot_utils.helpers.ast.builder.Ast__Python__Builder import Ast__Python__Builder
from osbot_utils.type_safe.Type_Safe                      import Type_Safe


class Ast__Code__Templates(Type_Safe):        # Predefined code templates

    def flask_app_template(self) -> Ast__Python__Builder:
        """Generate a basic Flask app"""
        return (Ast__Python__Builder()
            .add_from_import('flask', ['Flask', 'request', 'jsonify'])
            .add_variable('app', 'Flask(__name__)')
            .add_function('health_check')
                .add_decorator('@app.route("/health")')
                .returns_call('jsonify', [], {'status': '"healthy"'})
            .end_function()
            .add_if('__name__ == "__main__"')
                .call('app.run', [], {'debug': 'True'})
            .end_if())

    @staticmethod
    def test_class_template(class_to_test: str) -> Ast__Python__Builder:
        """Generate test class template"""
        return (Ast__Python__Builder()
            .add_import('unittest')
            .add_from_import('unittest.mock', ['patch', 'Mock'])
            .add_class(f'Test{class_to_test}')
                .inherits_from('unittest.TestCase')
                .add_method('setUp')
                    .assign(f'self.{class_to_test.lower()}', f'{class_to_test}()')
                .end_method()
                .add_method('test_placeholder')
                    .call('self.assertTrue', ['True'])
                .end_method()
            .end_class())