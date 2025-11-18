from unittest                                      import TestCase
from osbot_utils.type_safe.Type_Safe              import Type_Safe
from osbot_utils.testing.__                       import __, __SKIP__, __MISSING__
from typing                                       import Dict, List, Any


class test__using_Type_Safe(TestCase):

    @classmethod
    def setUpClass(cls):                                                                  # Define test Type_Safe classes
        class Schema__User(Type_Safe):
            user_id     : str
            name        : str
            email       : str
            age         : int
            is_active   : bool = True
            tags        : List[str]
            preferences : Dict[str, str]

        class Schema__Order(Type_Safe):
            order_id    : str
            user        : Schema__User
            items       : List[Dict[str, Any]]
            total       : float = 0.0
            status      : str = 'pending'

        class Schema__Complex(Type_Safe):
            id          : str
            nested      : Dict[str, Schema__User]
            users       : List[Schema__User]
            metadata    : dict

        cls.Schema__User    = Schema__User
        cls.Schema__Order   = Schema__Order
        cls.Schema__Complex = Schema__Complex

    def test__obj_returns_double_underscore(self):                                       # Test that .obj() returns __ instance
        with self.Schema__User() as user:
            obj = user.obj()
            assert type(obj).__name__ == '__'                                            # Returns __ class
            assert isinstance(obj, __)                                                   # Is instance of __

    def test__obj_basic_comparison(self):                                                # Test .obj() output for basic Type_Safe
        with self.Schema__User() as user:
            user.user_id = 'u-123'
            user.name    = 'Alice'
            user.email   = 'alice@test.com'
            user.age     = 25

            # Use .obj() with __ for comparison
            assert user.obj() == __(user_id     = 'u-123'                          ,
                                   name        = 'Alice'                           ,
                                   email       = 'alice@test.com'                  ,
                                   age         = 25                                ,
                                   is_active   = True                              ,    # Default value
                                   tags        = []                                ,    # Empty Type_Safe__List
                                   preferences = __()                              )    # Empty Type_Safe__Dict

    def test__obj_with_skip_for_dynamic_fields(self):                                   # Test using __SKIP__ with Type_Safe .obj()
        with self.Schema__User() as user:
            user.user_id = 'u-generated-456'
            user.name    = 'Bob'
            user.email   = 'bob@test.com'
            user.age     = 30

            # Can skip auto-generated fields
            assert user.obj() == __(user_id     = __SKIP__                         ,    # Skip generated ID
                                   name        = 'Bob'                             ,
                                   email       = 'bob@test.com'                    ,
                                   age         = 30                                ,
                                   is_active   = True                              ,
                                   tags        = []                                ,
                                   preferences = __()                                )

    def test__obj_contains_for_partial_matching(self):                                  # Test .contains() with Type_Safe .obj()
        with self.Schema__User() as user:
            user.user_id = 'u-789'
            user.name    = 'Charlie'
            user.email   = 'charlie@test.com'
            user.age     = 35
            user.tags    = ['admin', 'developer']

            # Partial matching with contains
            assert user.obj().contains(__(name='Charlie', age=35))
            assert user.obj().contains(__(email='charlie@test.com'))
            assert not user.obj().contains(__(name='David'))

    def test__obj_with_nested_type_safe(self):                                         # Test .obj() with nested Type_Safe objects
        with self.Schema__Order() as order:
            with self.Schema__User() as user:
                user.user_id = 'u-001'
                user.name    = 'Diana'
                user.email   = 'diana@test.com'
                user.age     = 28

                order.order_id = 'ord-001'
                order.user     = user
                order.items    = [{'product': 'laptop', 'qty': 1, 'price': 999.99}]  # BUG
                order.total    = 999.99
                # Nested Type_Safe becomes nested __ in .obj()
                assert order.obj() == __(order_id = 'ord-001'                      ,
                                       user     = __(user_id     = 'u-001'        ,
                                                    name        = 'Diana'          ,
                                                    email       = 'diana@test.com' ,
                                                    age         = 28               ,
                                                    is_active   = True             ,
                                                    tags        = []               ,
                                                    preferences = __()               ),
                                       items    = [__(product='laptop', qty=1, price=999.99)],
                                       total    = 999.99                          ,
                                       status   = 'pending'                       )

    def test__obj_excluding_for_timestamp_fields(self):                                 # Test excluding with Type_Safe .obj()
        with self.Schema__User() as user:
            user.user_id    = 'u-999'
            user.name       = 'Eve'
            user.email      = 'eve@test.com'
            user.age        = 40
            user.created_at = '2024-01-01T12:00:00Z'                                   # Simulate timestamp
            user.updated_at = '2024-01-02T15:30:00Z'                                   # Simulate timestamp

            # Exclude timestamps for comparison
            assert user.obj().excluding('created_at', 'updated_at') == __(
                user_id     = 'u-999'       ,
                name        = 'Eve'         ,
                email       = 'eve@test.com',
                age         = 40            ,
                is_active   = True          ,
                tags        = []            ,
                preferences = __()
            )

    def test__obj_diff_for_debugging(self):                                            # Test diff with Type_Safe .obj()
        with self.Schema__User() as user1:
            user1.user_id = 'u-100'
            user1.name    = 'Frank'
            user1.email   = 'frank@test.com'
            user1.age     = 25

        with self.Schema__User() as user2:
            user2.user_id = 'u-100'
            user2.name    = 'Frank'
            user2.email   = 'frank@different.com'                                      # Different email
            user2.age     = 26                                                         # Different age

        diff = user1.obj().diff(user2.obj())
        assert diff == __(email = __(actual='frank@test.com', expected='frank@different.com'),
                          age   = __(actual=25, expected=26))

    def test__obj_merge_for_test_variations(self):                                     # Test merge with Type_Safe .obj()
        with self.Schema__User() as base_user:
            base_user.user_id = 'u-base'
            base_user.name    = 'Base User'
            base_user.email   = 'base@test.com'
            base_user.age     = 30

            # Create variation using merge
            admin_variation = base_user.obj().merge(
                name      = 'Admin User',
                is_active = True,
                tags      = ['admin', 'super_user']
            )

            assert admin_variation.name      == 'Admin User'                          # Changed
            assert admin_variation.email     == 'base@test.com'                       # Preserved
            assert admin_variation.tags      == ['admin', 'super_user']               # Added

    def test__obj_with_type_safe_collections(self):                                    # Test Type_Safe collections in .obj()
        with self.Schema__User() as user:
            user.user_id = 'u-collections'
            user.name    = 'Grace'
            user.email   = 'grace@test.com'
            user.age     = 32

            # Type_Safe__List operations
            user.tags.append('developer')
            user.tags.append('team_lead')

            # Type_Safe__Dict operations
            user.preferences['theme'] = 'dark'
            user.preferences['lang']  = 'en'

            obj = user.obj()

            # Collections are converted to regular list/dict in .obj()
            assert obj.tags        == ['developer', 'team_lead']
            assert obj.preferences == __(theme='dark', lang='en')

            # Can still use __ methods on the result
            assert obj.contains(__(tags=['developer', 'team_lead']))

    def test__obj_with_complex_nested_structures(self):                                # Test complex nested Type_Safe
        with self.Schema__Complex() as complex_obj:
            complex_obj.id = 'complex-1'

            # Create nested users
            with self.Schema__User() as user1:
                user1.user_id = 'u-nested-1'
                user1.name    = 'Nested User 1'
                user1.email   = 'nested1@test.com'
                user1.age     = 25

            with self.Schema__User() as user2:
                user2.user_id = 'u-nested-2'
                user2.name    = 'Nested User 2'
                user2.email   = 'nested2@test.com'
                user2.age     = 30

            complex_obj.nested['first']  = user1
            complex_obj.nested['second'] = user2
            complex_obj.users.append(user1)
            complex_obj.users.append(user2)
            complex_obj.metadata = {'created': '2024-01-01', 'version': '1.0'}

            obj = complex_obj.obj()

            # Verify nested structure with partial matching
            assert obj.contains(__(id='complex-1'))
            assert obj.nested.first.name  == 'Nested User 1'
            assert obj.nested.second.name == 'Nested User 2'
            assert len(obj.users) == 2
            assert obj.users[0].user_id == 'u-nested-1'

    def test__real_world_pattern__api_request_validation(self):                       # Real-world: validating API requests
        with self.Schema__Order() as order:
            with self.Schema__User() as user:
                user.user_id = 'api-user-123'
                user.name    = 'API Test User'
                user.email   = 'api@test.com'
                user.age     = 25

            order.order_id = 'api-order-456'
            order.user     = user
            order.items    = [
                {'product': 'item1', 'qty': 2, 'price': 50.00},
                {'product': 'item2', 'qty': 1, 'price': 75.00}
            ]
            order.total    = 175.00
            order.status   = 'processing'

            # Validate structure without caring about IDs
            expected_structure = __(
                order_id = __SKIP__,                                                   # Skip generated ID
                user     = __(user_id   = __SKIP__,                                   # Skip user ID
                             name      = 'API Test User',
                             email     = 'api@test.com',
                             age       = 25,
                             is_active = True,
                             tags      = [],
                             preferences = __()),
                items    = __SKIP__,                                                   # Skip items detail
                total    = 175.00,
                status   = 'processing'
            )

            assert order.obj() == expected_structure

    def test__real_world_pattern__test_data_builder(self):                           # Real-world: building test data
        # Create base test user
        with self.Schema__User() as base_user:
            base_user.user_id = 'test-base'
            base_user.name    = 'Test User'
            base_user.email   = 'test@example.com'
            base_user.age     = 30

        # Build variations for different test scenarios
        admin_user = base_user.obj().merge(
            user_id = 'test-admin',
            name    = 'Admin User',
            tags    = ['admin', 'moderator']
        )

        inactive_user = base_user.obj().merge(
            user_id   = 'test-inactive',
            is_active = False,
            tags      = ['suspended']
        )

        premium_user = base_user.obj().merge(
            user_id     = 'test-premium',
            tags        = ['premium', 'verified'],
            preferences = {'subscription': 'premium', 'billing': 'annual'}
        )

        # Verify variations
        assert admin_user.tags         == ['admin', 'moderator']
        assert inactive_user.is_active == False
        assert premium_user.preferences['subscription'] == 'premium'

        # All variations still have base properties
        assert admin_user.email    == 'test@example.com'
        assert inactive_user.email == 'test@example.com'
        assert premium_user.email  == 'test@example.com'

    def test__real_world_pattern__response_transformation(self):                      # Real-world: API response testing
        # Simulate service that returns Type_Safe objects
        def get_user_with_orders(user_id):
            with self.Schema__User() as user:
                user.user_id = user_id
                user.name    = 'Service User'
                user.email   = 'service@test.com'
                user.age     = 35
                user.tags    = ['customer', 'verified']

            orders = []
            for i in range(3):
                with self.Schema__Order() as order:
                    order.order_id = f'ord-{i}'
                    order.user     = user
                    order.items    = [{'product': f'item-{i}', 'qty': 1}]
                    order.total    = 100.00 * (i + 1)
                    orders.append(order)

            return {'user': user, 'orders': orders}

        # Test the response
        response = get_user_with_orders('u-service-001')

        # Convert to __ for testing
        user_obj   = response['user'].obj()
        orders_obj = [order.obj() for order in response['orders']]

        # Verify user structure
        assert user_obj.contains(__(
            name  = 'Service User',
            email = 'service@test.com',
            tags  = ['customer', 'verified']
        ))

        # Verify orders
        assert len(orders_obj) == 3
        assert orders_obj[0].total == 100.00
        assert orders_obj[1].total == 200.00
        assert orders_obj[2].total == 300.00

        # All orders reference the same user
        for order_obj in orders_obj:
            assert order_obj.user.user_id == 'u-service-001'

    def test__integration__type_safe_roundtrip_with_obj(self):                       # Test Type_Safe -> __ -> comparison
        with self.Schema__User() as original:
            original.user_id     = 'roundtrip-1'
            original.name        = 'Roundtrip User'
            original.email       = 'roundtrip@test.com'
            original.age         = 28
            original.tags        = ['test', 'roundtrip']
            original.preferences = {'setting1': 'value1', 'setting2': 'value2'}

        # Convert to __ and back to dict
        obj_version  = original.obj()
        json_version = original.json()

        # Create new Type_Safe from json
        with self.Schema__User.from_json(json_version) as restored:
            # Compare using .obj()
            assert restored.obj() == obj_version                                      # Perfect roundtrip

            # Test modifications using __
            modified = obj_version.merge(name='Modified User', age=29)

            # Verify original unchanged
            assert original.name == 'Roundtrip User'
            assert original.age  == 28

            # Verify modification
            assert modified.name == 'Modified User'
            assert modified.age  == 29

    def test__edge_case__empty_type_safe(self):                                      # Test empty Type_Safe objects
        with self.Schema__User() as empty_user:
            obj = empty_user.obj()

            # All fields have default/empty values
            assert obj.user_id     == ''                                              # Empty string
            assert obj.name        == ''                                              # Empty string
            assert obj.email       == ''                                              # Empty string
            assert obj.age         == 0                                               # Zero
            assert obj.is_active   == True                                            # Default True
            assert obj.tags        == []                                              # Empty list
            assert obj.preferences == __()                                            # Empty dict

            # Can still use __ methods
            assert obj.contains(__(is_active=True))
            assert obj.excluding('user_id', 'name', 'email', 'age').tags == []