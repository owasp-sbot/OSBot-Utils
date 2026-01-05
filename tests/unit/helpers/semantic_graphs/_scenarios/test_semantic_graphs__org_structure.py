# ═══════════════════════════════════════════════════════════════════════════════
# Test Semantic Graphs - Organizational Structure Scenario
#
# Demonstrates semantic graphs for company organization:
#   - Taxonomy: organizational_unit → department, team, role
#   - Ontology: company, department, team, employee with relationships
#   - Rules: employees must have manager, teams must have lead
#   - Graph: company org chart representation
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                   import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Id             import Dict__Categories__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Id             import Dict__Node_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id                  import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicates__By_Id             import Dict__Predicates__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Names__By_Id         import Dict__Property_Names__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Types__By_Id         import Dict__Property_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Ids                  import List__Category_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Edge_Rules                    import List__Edge_Rules
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Required_Node_Property import List__Rules__Required_Node_Property
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges         import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                         import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                        import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                        import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                       import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                         import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref                        import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                        import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref                       import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id                    import Property_Name_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Ref                   import Property_Name_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Id                    import Property_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Ref                   import Property_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                         import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref                        import Rule_Set_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                         import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref                        import Taxonomy_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                      import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Edge_Rule           import Schema__Ontology__Edge_Rule
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type           import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Predicate           import Schema__Ontology__Predicate
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Property_Name       import Schema__Ontology__Property_Name
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Property_Type       import Schema__Ontology__Property_Type
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                          import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Node_Property      import Schema__Rule__Required_Node_Property
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph                   import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge             import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node             import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy                      import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category            import Schema__Taxonomy__Category
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Utils                               import Ontology__Utils
from osbot_utils.helpers.semantic_graphs.taxonomy.Taxonomy__Utils                               import Taxonomy__Utils
from osbot_utils.helpers.semantic_graphs.rule.Rule_Set__Utils                                   import Rule_Set__Utils
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                import Obj_Id


class test_semantic_graphs__org_structure(TestCase):                                   # Org structure scenario

    @classmethod
    def setUpClass(cls):                                                               # Build complete org model
        cls.build_taxonomy()
        cls.build_ontology()
        cls.build_rule_set()
        cls.build_graph()

    # ═══════════════════════════════════════════════════════════════════════════
    # Model Construction
    # ═══════════════════════════════════════════════════════════════════════════

    @classmethod
    def build_taxonomy(cls):                                                           # Create org unit taxonomy
        # Category IDs
        cls.cat_root_id       = Category_Id(Obj_Id.from_seed('org:cat:root'))
        cls.cat_structural_id = Category_Id(Obj_Id.from_seed('org:cat:structural'))
        cls.cat_people_id     = Category_Id(Obj_Id.from_seed('org:cat:people'))
        cls.cat_role_id       = Category_Id(Obj_Id.from_seed('org:cat:role'))

        # Build hierarchy
        cat_root = Schema__Taxonomy__Category(
            category_id  = cls.cat_root_id                                              ,
            category_ref = Category_Ref('org_entity')                                   ,
            parent_id    = None                                                         ,
            child_ids    = List__Category_Ids([cls.cat_structural_id, cls.cat_people_id, cls.cat_role_id])
        )
        cat_structural = Schema__Taxonomy__Category(
            category_id  = cls.cat_structural_id                                        ,
            category_ref = Category_Ref('structural')                                   ,
            parent_id    = cls.cat_root_id                                              ,
            child_ids    = List__Category_Ids()
        )
        cat_people = Schema__Taxonomy__Category(
            category_id  = cls.cat_people_id                                            ,
            category_ref = Category_Ref('people')                                       ,
            parent_id    = cls.cat_root_id                                              ,
            child_ids    = List__Category_Ids()
        )
        cat_role = Schema__Taxonomy__Category(
            category_id  = cls.cat_role_id                                              ,
            category_ref = Category_Ref('role')                                         ,
            parent_id    = cls.cat_root_id                                              ,
            child_ids    = List__Category_Ids()
        )

        categories = Dict__Categories__By_Id()
        categories[cls.cat_root_id]       = cat_root
        categories[cls.cat_structural_id] = cat_structural
        categories[cls.cat_people_id]     = cat_people
        categories[cls.cat_role_id]       = cat_role

        cls.taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('org:taxonomy'))
        cls.taxonomy = Schema__Taxonomy(
            taxonomy_id  = cls.taxonomy_id                                              ,
            taxonomy_ref = Taxonomy_Ref('org_structure')                                ,
            root_id      = cls.cat_root_id                                              ,
            categories   = categories
        )

    @classmethod
    def build_ontology(cls):                                                           # Create org ontology
        # Node Type IDs
        cls.nt_company_id    = Node_Type_Id(Obj_Id.from_seed('org:nt:company'))
        cls.nt_department_id = Node_Type_Id(Obj_Id.from_seed('org:nt:department'))
        cls.nt_team_id       = Node_Type_Id(Obj_Id.from_seed('org:nt:team'))
        cls.nt_employee_id   = Node_Type_Id(Obj_Id.from_seed('org:nt:employee'))
        cls.nt_role_id       = Node_Type_Id(Obj_Id.from_seed('org:nt:role'))

        # Predicate IDs
        cls.pred_contains_id    = Predicate_Id(Obj_Id.from_seed('org:pred:contains'))
        cls.pred_belongs_to_id  = Predicate_Id(Obj_Id.from_seed('org:pred:belongs_to'))
        cls.pred_reports_to_id  = Predicate_Id(Obj_Id.from_seed('org:pred:reports_to'))
        cls.pred_manages_id     = Predicate_Id(Obj_Id.from_seed('org:pred:manages'))
        cls.pred_has_role_id    = Predicate_Id(Obj_Id.from_seed('org:pred:has_role'))
        cls.pred_member_of_id   = Predicate_Id(Obj_Id.from_seed('org:pred:member_of'))

        # Property Type IDs
        cls.pt_string_id = Property_Type_Id(Obj_Id.from_seed('org:pt:string'))
        cls.pt_date_id   = Property_Type_Id(Obj_Id.from_seed('org:pt:date'))

        # Property Name IDs
        cls.pn_email_id      = Property_Name_Id(Obj_Id.from_seed('org:pn:email'))
        cls.pn_hire_date_id  = Property_Name_Id(Obj_Id.from_seed('org:pn:hire_date'))
        cls.pn_title_id      = Property_Name_Id(Obj_Id.from_seed('org:pn:title'))

        # Node Types
        node_types = Dict__Node_Types__By_Id()
        node_types[cls.nt_company_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_company_id                                           ,
            node_type_ref = Node_Type_Ref('company')                                    ,
            category_id   = cls.cat_structural_id
        )
        node_types[cls.nt_department_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_department_id                                        ,
            node_type_ref = Node_Type_Ref('department')                                 ,
            category_id   = cls.cat_structural_id
        )
        node_types[cls.nt_team_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_team_id                                              ,
            node_type_ref = Node_Type_Ref('team')                                       ,
            category_id   = cls.cat_structural_id
        )
        node_types[cls.nt_employee_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_employee_id                                          ,
            node_type_ref = Node_Type_Ref('employee')                                   ,
            category_id   = cls.cat_people_id
        )
        node_types[cls.nt_role_id] = Schema__Ontology__Node_Type(
            node_type_id  = cls.nt_role_id                                              ,
            node_type_ref = Node_Type_Ref('role')                                       ,
            category_id   = cls.cat_role_id
        )

        # Predicates (with inverses)
        predicates = Dict__Predicates__By_Id()
        predicates[cls.pred_contains_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_contains_id                                        ,
            predicate_ref = Predicate_Ref('contains')                                   ,
            inverse_id    = cls.pred_belongs_to_id
        )
        predicates[cls.pred_belongs_to_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_belongs_to_id                                      ,
            predicate_ref = Predicate_Ref('belongs_to')                                 ,
            inverse_id    = cls.pred_contains_id
        )
        predicates[cls.pred_reports_to_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_reports_to_id                                      ,
            predicate_ref = Predicate_Ref('reports_to')                                 ,
            inverse_id    = cls.pred_manages_id
        )
        predicates[cls.pred_manages_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_manages_id                                         ,
            predicate_ref = Predicate_Ref('manages')                                    ,
            inverse_id    = cls.pred_reports_to_id
        )
        predicates[cls.pred_has_role_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_has_role_id                                        ,
            predicate_ref = Predicate_Ref('has_role')                                   ,
            inverse_id    = None
        )
        predicates[cls.pred_member_of_id] = Schema__Ontology__Predicate(
            predicate_id  = cls.pred_member_of_id                                       ,
            predicate_ref = Predicate_Ref('member_of')                                  ,
            inverse_id    = None
        )

        # Property Types
        property_types = Dict__Property_Types__By_Id()
        property_types[cls.pt_string_id] = Schema__Ontology__Property_Type(
            property_type_id  = cls.pt_string_id                                        ,
            property_type_ref = Property_Type_Ref('string')
        )
        property_types[cls.pt_date_id] = Schema__Ontology__Property_Type(
            property_type_id  = cls.pt_date_id                                          ,
            property_type_ref = Property_Type_Ref('date')
        )

        # Property Names
        property_names = Dict__Property_Names__By_Id()
        property_names[cls.pn_email_id] = Schema__Ontology__Property_Name(
            property_name_id  = cls.pn_email_id                                         ,
            property_name_ref = Property_Name_Ref('email')                              ,
            property_type_id  = cls.pt_string_id
        )
        property_names[cls.pn_hire_date_id] = Schema__Ontology__Property_Name(
            property_name_id  = cls.pn_hire_date_id                                     ,
            property_name_ref = Property_Name_Ref('hire_date')                          ,
            property_type_id  = cls.pt_date_id
        )
        property_names[cls.pn_title_id] = Schema__Ontology__Property_Name(
            property_name_id  = cls.pn_title_id                                         ,
            property_name_ref = Property_Name_Ref('title')                              ,
            property_type_id  = cls.pt_string_id
        )

        # Edge Rules
        edge_rules = List__Edge_Rules()
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_company_id,    predicate_id=cls.pred_contains_id,   target_type_id=cls.nt_department_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_department_id, predicate_id=cls.pred_contains_id,   target_type_id=cls.nt_team_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_employee_id,   predicate_id=cls.pred_member_of_id,  target_type_id=cls.nt_team_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_employee_id,   predicate_id=cls.pred_reports_to_id, target_type_id=cls.nt_employee_id))
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id=cls.nt_employee_id,   predicate_id=cls.pred_has_role_id,   target_type_id=cls.nt_role_id))

        cls.ontology_id = Ontology_Id(Obj_Id.from_seed('org:ontology'))
        cls.ontology = Schema__Ontology(
            ontology_id    = cls.ontology_id                                            ,
            ontology_ref   = Ontology_Ref('org_structure')                              ,
            taxonomy_id    = cls.taxonomy_id                                            ,
            node_types     = node_types                                                 ,
            predicates     = predicates                                                 ,
            property_types = property_types                                             ,
            property_names = property_names                                             ,
            edge_rules     = edge_rules
        )

    @classmethod
    def build_rule_set(cls):                                                           # Create validation rules
        required_node_properties = List__Rules__Required_Node_Property()
        required_node_properties.append(Schema__Rule__Required_Node_Property(
            node_type_id     = cls.nt_employee_id                                       ,
            property_name_id = cls.pn_email_id                                          ,
            required         = True
        ))
        required_node_properties.append(Schema__Rule__Required_Node_Property(
            node_type_id     = cls.nt_employee_id                                       ,
            property_name_id = cls.pn_hire_date_id                                      ,
            required         = True
        ))

        cls.rule_set_id = Rule_Set_Id(Obj_Id.from_seed('org:rules'))
        cls.rule_set = Schema__Rule_Set(
            rule_set_id              = cls.rule_set_id                                  ,
            rule_set_ref             = Rule_Set_Ref('org_validation')                   ,
            ontology_id              = cls.ontology_id                                  ,
            required_node_properties = required_node_properties
        )

    @classmethod
    def build_graph(cls):                                                              # Create sample org chart
        # Node IDs
        cls.node_company_id   = Node_Id(Obj_Id.from_seed('org:node:company'))
        cls.node_eng_dept_id  = Node_Id(Obj_Id.from_seed('org:node:eng_dept'))
        cls.node_backend_id   = Node_Id(Obj_Id.from_seed('org:node:backend'))
        cls.node_frontend_id  = Node_Id(Obj_Id.from_seed('org:node:frontend'))
        cls.node_cto_id       = Node_Id(Obj_Id.from_seed('org:node:cto'))
        cls.node_lead1_id     = Node_Id(Obj_Id.from_seed('org:node:lead1'))
        cls.node_lead2_id     = Node_Id(Obj_Id.from_seed('org:node:lead2'))
        cls.node_dev1_id      = Node_Id(Obj_Id.from_seed('org:node:dev1'))
        cls.node_dev2_id      = Node_Id(Obj_Id.from_seed('org:node:dev2'))

        # Nodes
        nodes = Dict__Nodes__By_Id()
        nodes[cls.node_company_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_company_id                                          ,
            node_type_id = cls.nt_company_id                                            ,
            name         = 'Acme Corp'
        )
        nodes[cls.node_eng_dept_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_eng_dept_id                                         ,
            node_type_id = cls.nt_department_id                                         ,
            name         = 'Engineering'
        )
        nodes[cls.node_backend_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_backend_id                                          ,
            node_type_id = cls.nt_team_id                                               ,
            name         = 'Backend Team'
        )
        nodes[cls.node_frontend_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_frontend_id                                         ,
            node_type_id = cls.nt_team_id                                               ,
            name         = 'Frontend Team'
        )
        nodes[cls.node_cto_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_cto_id                                              ,
            node_type_id = cls.nt_employee_id                                           ,
            name         = 'Jane Smith (CTO)'
        )
        nodes[cls.node_lead1_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_lead1_id                                            ,
            node_type_id = cls.nt_employee_id                                           ,
            name         = 'Bob Johnson (Backend Lead)'
        )
        nodes[cls.node_lead2_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_lead2_id                                            ,
            node_type_id = cls.nt_employee_id                                           ,
            name         = 'Alice Brown (Frontend Lead)'
        )
        nodes[cls.node_dev1_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_dev1_id                                             ,
            node_type_id = cls.nt_employee_id                                           ,
            name         = 'Charlie Wilson'
        )
        nodes[cls.node_dev2_id] = Schema__Semantic_Graph__Node(
            node_id      = cls.node_dev2_id                                             ,
            node_type_id = cls.nt_employee_id                                           ,
            name         = 'Diana Lee'
        )

        # Edges
        edges = List__Semantic_Graph__Edges()
        # Containment hierarchy
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_company_id,  predicate_id=cls.pred_contains_id,   to_node_id=cls.node_eng_dept_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_eng_dept_id, predicate_id=cls.pred_contains_id,   to_node_id=cls.node_backend_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_eng_dept_id, predicate_id=cls.pred_contains_id,   to_node_id=cls.node_frontend_id))
        # Team membership
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_lead1_id,    predicate_id=cls.pred_member_of_id,  to_node_id=cls.node_backend_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_dev1_id,     predicate_id=cls.pred_member_of_id,  to_node_id=cls.node_backend_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_lead2_id,    predicate_id=cls.pred_member_of_id,  to_node_id=cls.node_frontend_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_dev2_id,     predicate_id=cls.pred_member_of_id,  to_node_id=cls.node_frontend_id))
        # Reporting hierarchy
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_lead1_id,    predicate_id=cls.pred_reports_to_id, to_node_id=cls.node_cto_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_lead2_id,    predicate_id=cls.pred_reports_to_id, to_node_id=cls.node_cto_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_dev1_id,     predicate_id=cls.pred_reports_to_id, to_node_id=cls.node_lead1_id))
        edges.append(Schema__Semantic_Graph__Edge(from_node_id=cls.node_dev2_id,     predicate_id=cls.pred_reports_to_id, to_node_id=cls.node_lead2_id))

        cls.graph_id = Graph_Id(Obj_Id.from_seed('org:graph'))
        cls.graph = Schema__Semantic_Graph(
            graph_id    = cls.graph_id                                                  ,
            ontology_id = cls.ontology_id                                               ,
            nodes       = nodes                                                         ,
            edges       = edges
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # Structure Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__graph__node_counts_by_type(self):                                        # Count nodes by type
        type_counts = {}
        for node in self.graph.nodes.values():
            type_id = str(node.node_type_id)
            type_counts[type_id] = type_counts.get(type_id, 0) + 1

        # Should have: 1 company, 1 department, 2 teams, 5 employees
        assert len(self.graph.nodes) == 9

    def test__graph__employee_nodes(self):                                             # Test employee nodes
        employees = [n for n in self.graph.nodes.values() if n.node_type_id == self.nt_employee_id]
        assert len(employees) == 5

        names = [e.name  for e in employees]
        assert 'Jane Smith (CTO)' in names
        assert 'Charlie Wilson' in names

    def test__graph__containment_hierarchy(self):                                      # Test containment edges
        contains_edges = [e for e in self.graph.edges if e.predicate_id == self.pred_contains_id]
        assert len(contains_edges) == 3  # company→dept, dept→team1, dept→team2

    def test__graph__reporting_chain(self):                                            # Test reporting relationships
        reports_to_edges = [e for e in self.graph.edges if e.predicate_id == self.pred_reports_to_id]
        assert len(reports_to_edges) == 4

        # Find who reports to CTO
        cto_reports = [e for e in reports_to_edges if e.to_node_id == self.node_cto_id]
        assert len(cto_reports) == 2  # Both leads report to CTO

    def test__graph__team_membership(self):                                            # Test team membership
        member_of_edges = [e for e in self.graph.edges if e.predicate_id == self.pred_member_of_id]
        assert len(member_of_edges) == 4

        # Backend team members
        backend_members = [e.from_node_id for e in member_of_edges if e.to_node_id == self.node_backend_id]
        assert len(backend_members) == 2
        assert self.node_lead1_id in backend_members
        assert self.node_dev1_id in backend_members

    # ═══════════════════════════════════════════════════════════════════════════
    # Ontology Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__ontology__valid_edges(self):                                             # Test edge rule validation
        utils = Ontology__Utils()

        # Valid org relationships
        assert utils.is_valid_edge(self.ontology, self.nt_company_id,    self.pred_contains_id,   self.nt_department_id)
        assert utils.is_valid_edge(self.ontology, self.nt_department_id, self.pred_contains_id,   self.nt_team_id)
        assert utils.is_valid_edge(self.ontology, self.nt_employee_id,   self.pred_reports_to_id, self.nt_employee_id)
        assert utils.is_valid_edge(self.ontology, self.nt_employee_id,   self.pred_member_of_id,  self.nt_team_id)

        # Invalid relationships
        assert not utils.is_valid_edge(self.ontology, self.nt_team_id, self.pred_contains_id, self.nt_company_id)
        assert not utils.is_valid_edge(self.ontology, self.nt_team_id, self.pred_reports_to_id, self.nt_employee_id)

    def test__ontology__inverse_predicates(self):                                      # Test inverse predicate lookup
        utils = Ontology__Utils()

        # contains ↔ belongs_to
        assert utils.get_inverse_predicate(self.ontology, self.pred_contains_id).predicate_id == self.pred_belongs_to_id
        assert utils.get_inverse_predicate(self.ontology, self.pred_belongs_to_id).predicate_id == self.pred_contains_id

        # reports_to ↔ manages
        assert utils.get_inverse_predicate(self.ontology, self.pred_reports_to_id).predicate_id == self.pred_manages_id
        assert utils.get_inverse_predicate(self.ontology, self.pred_manages_id).predicate_id == self.pred_reports_to_id

    # ═══════════════════════════════════════════════════════════════════════════
    # Rule Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__rules__employee_required_properties(self):                               # Test employee property rules
        utils = Rule_Set__Utils()

        # Employees require email and hire_date
        required = utils.get_required_properties_for_node_type(self.rule_set, self.nt_employee_id)
        assert len(required) == 2
        assert self.pn_email_id in required
        assert self.pn_hire_date_id in required

    def test__rules__other_types_no_requirements(self):                                # Test non-employee types
        utils = Rule_Set__Utils()

        # Other types have no required properties
        assert len(utils.get_required_properties_for_node_type(self.rule_set, self.nt_company_id)) == 0
        assert len(utils.get_required_properties_for_node_type(self.rule_set, self.nt_team_id)) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Taxonomy Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__taxonomy__category_node_type_mapping(self):                              # Test node types linked to categories
        ont_utils = Ontology__Utils()
        tax_utils = Taxonomy__Utils()

        # Get employee node type
        employee_type = ont_utils.get_node_type(self.ontology, self.nt_employee_id)
        assert employee_type.category_id == self.cat_people_id

        # Get category info
        people_cat = tax_utils.get_category(self.taxonomy, self.cat_people_id)
        assert str(people_cat.category_ref) == 'people'

        # Verify category is descendant of root
        assert tax_utils.is_descendant_of(self.taxonomy, self.cat_people_id, self.cat_root_id)