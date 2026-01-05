# ═══════════════════════════════════════════════════════════════════════════════
# Semantic_Graph__Projector - Transforms Schema__ to Projected__
#
# Updated for Brief 3.8:
#   - Projects properties on nodes and edges (ID → Ref)
#   - Builds filtered references (only used refs)
#   - Builds taxonomy section (node type → category mapping)
#   - Requires access to Taxonomy__Registry to resolve category IDs
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Registry                             import Ontology__Registry
from osbot_utils.helpers.semantic_graphs.taxonomy.Taxonomy__Registry                             import Taxonomy__Registry
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Category_Ids__By_Ref           import Dict__Category_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Category_Refs__By_Category_Ref import Dict__Category_Refs__By_Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Category_Refs__By_Node_Type_Ref import Dict__Category_Refs__By_Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Type_Ids__By_Ref          import Dict__Node_Type_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicate_Ids__By_Ref          import Dict__Predicate_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Projected_Properties           import Dict__Projected_Properties
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Name_Ids__By_Ref      import Dict__Property_Name_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Type_Ids__By_Ref      import Dict__Property_Type_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Projected__Edges               import List__Projected__Edges
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Projected__Nodes               import List__Projected__Nodes
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph                    import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                         import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                        import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref                        import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Ref                    import Property_Name_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                       import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Data               import Schema__Projected__Data
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Edge               import Schema__Projected__Edge
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Node               import Schema__Projected__Node
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__References         import Schema__Projected__References
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Semantic_Graph     import Schema__Projected__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Sources            import Schema__Projected__Sources
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Taxonomy           import Schema__Projected__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy                       import Schema__Taxonomy
from osbot_utils.type_safe.Type_Safe                                                             import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now                 import Timestamp_Now
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                  import Safe_Str__Id
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                   import type_safe


class Semantic_Graph__Projector(Type_Safe):                                          # Schema__ → Projected__ transformer
    ontology_registry : Ontology__Registry                                           # For resolving IDs to refs
    taxonomy_registry : Taxonomy__Registry = None                                    # For resolving category IDs

    @type_safe
    def project(self, graph: Schema__Semantic_Graph) -> Schema__Projected__Semantic_Graph:   # Generate projection from schema
        ontology = self.ontology_registry.get_by_id(graph.ontology_id)               # Get ontology for lookups
        taxonomy = self.get_taxonomy(ontology)                                       # Get taxonomy if available
        if ontology is None:
            return Schema__Projected__Semantic_Graph()
        # Build lookup maps
        node_type_id_to_ref     = self.build_node_type_id_to_ref(ontology)
        predicate_id_to_ref     = self.build_predicate_id_to_ref(ontology)
        property_name_id_to_ref = self.build_property_name_id_to_ref(ontology)
        node_id_to_name         = self.build_node_id_to_name(graph)

        # Project nodes and edges
        projected_nodes = self.project_nodes(graph, node_type_id_to_ref, property_name_id_to_ref)
        projected_edges = self.project_edges(graph, node_id_to_name, predicate_id_to_ref, property_name_id_to_ref)

        # Build filtered references (only what's used)
        references = self.build_references_filtered(ontology, taxonomy, projected_nodes, projected_edges)

        # Build taxonomy section
        taxonomy_section = self.build_taxonomy_section(ontology, taxonomy, projected_nodes)

        # Build sources
        sources = self.build_sources(graph, ontology)

        return Schema__Projected__Semantic_Graph(projection = Schema__Projected__Data(nodes = projected_nodes,
                                                                                      edges = projected_edges),
                                                 references = references                                       ,
                                                 taxonomy   = taxonomy_section                                 ,
                                                 sources    = sources                                          )

    # ═══════════════════════════════════════════════════════════════════════════
    # Taxonomy Lookup
    # ═══════════════════════════════════════════════════════════════════════════

    def get_taxonomy(self, ontology: Schema__Ontology) -> Schema__Taxonomy:          # Get taxonomy from registry
        if ontology is None or ontology.taxonomy_id is None:
            return None
        if self.taxonomy_registry is None:
            return None
        return self.taxonomy_registry.get_by_id(ontology.taxonomy_id)

    # ═══════════════════════════════════════════════════════════════════════════
    # Reverse Lookup Builders
    # ═══════════════════════════════════════════════════════════════════════════

    def build_node_type_id_to_ref(self, ontology: Schema__Ontology) -> dict:         # Build ID → Ref map for node types
        if ontology is None:
            return {}
        return {nt.node_type_id: nt.node_type_ref for nt in ontology.node_types.values()}

    def build_predicate_id_to_ref(self, ontology: Schema__Ontology) -> dict:         # Build ID → Ref map for predicates
        if ontology is None:
            return {}
        return {p.predicate_id: p.predicate_ref for p in ontology.predicates.values()}

    def build_property_name_id_to_ref(self, ontology: Schema__Ontology) -> dict:     # Build ID → Ref map for property names
        if ontology is None:
            return {}
        return {pn.property_name_id: pn.property_name_ref for pn in ontology.property_names.values()}

    def build_node_id_to_name(self, graph: Schema__Semantic_Graph) -> dict:          # Build Node_Id → name map
        return {node.node_id: node.name for node in graph.nodes.values()}

    # ═══════════════════════════════════════════════════════════════════════════
    # Projection Methods
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def project_nodes(self                          ,
                      graph                   : Schema__Semantic_Graph,
                      node_type_id_to_ref     : dict                  ,
                      property_name_id_to_ref : dict                  ) -> List__Projected__Nodes:
        result = List__Projected__Nodes()
        for node in graph.nodes.values():
            ref        = node_type_id_to_ref.get(node.node_type_id, Node_Type_Ref(''))
            properties = self.project_properties(node.properties, property_name_id_to_ref)
            result.append(Schema__Projected__Node(ref        = ref        ,
                                                  name       = node.name  ,
                                                  properties = properties ))
        return result

    @type_safe
    def project_edges(self                          ,
                      graph                   : Schema__Semantic_Graph,
                      node_id_to_name         : dict                  ,
                      predicate_id_to_ref     : dict                  ,
                      property_name_id_to_ref : dict                  ) -> List__Projected__Edges:
        result = List__Projected__Edges()
        for edge in graph.edges:
            from_name  = node_id_to_name.get(edge.from_node_id, Safe_Str__Id(''))
            to_name    = node_id_to_name.get(edge.to_node_id  , Safe_Str__Id(''))
            ref        = predicate_id_to_ref.get(edge.predicate_id, Predicate_Ref(''))
            properties = self.project_properties(edge.properties, property_name_id_to_ref)
            result.append(Schema__Projected__Edge(from_name  = from_name  ,
                                                  to_name    = to_name    ,
                                                  ref        = ref        ,
                                                  properties = properties ))
        return result

    def project_properties(self                          ,
                           properties             : dict ,
                           property_name_id_to_ref: dict ) -> Dict__Projected_Properties:  # Project properties ID → Ref
        if properties is None:
            return None
        result = Dict__Projected_Properties()
        for prop_id, value in properties.items():
            prop_ref = property_name_id_to_ref.get(prop_id, Property_Name_Ref(''))
            result[prop_ref] = value
        return result

    # ═══════════════════════════════════════════════════════════════════════════
    # Filtered References Builder
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def build_references_filtered(self                                     ,
                                  ontology        : Schema__Ontology       ,
                                  taxonomy        : Schema__Taxonomy       ,
                                  projected_nodes : List__Projected__Nodes ,
                                  projected_edges : List__Projected__Edges ) -> Schema__Projected__References:
        # Collect used refs from projection
        used_node_type_refs = set()
        used_property_refs  = set()
        for node in projected_nodes:
            if node.ref:
                used_node_type_refs.add(node.ref)
            if node.properties:
                for prop_ref in node.properties.keys():
                    used_property_refs.add(prop_ref)

        used_predicate_refs = set()
        for edge in projected_edges:
            if edge.ref:
                used_predicate_refs.add(edge.ref)
            if edge.properties:
                for prop_ref in edge.properties.keys():
                    used_property_refs.add(prop_ref)

        # Build filtered node_types
        node_types = Dict__Node_Type_Ids__By_Ref()
        if ontology:
            for nt in ontology.node_types.values():
                if nt.node_type_ref in used_node_type_refs:
                    node_types[nt.node_type_ref] = nt.node_type_id

        # Build filtered predicates
        predicates = Dict__Predicate_Ids__By_Ref()
        if ontology:
            for p in ontology.predicates.values():
                if p.predicate_ref in used_predicate_refs:
                    predicates[p.predicate_ref] = p.predicate_id

        # Build filtered property_names and collect used type IDs
        property_names    = Dict__Property_Name_Ids__By_Ref()
        used_type_ids     = set()
        if ontology:
            for pn in ontology.property_names.values():
                if pn.property_name_ref in used_property_refs:
                    property_names[pn.property_name_ref] = pn.property_name_id
                    if pn.property_type_id:
                        used_type_ids.add(pn.property_type_id)

        # Build filtered property_types
        property_types = Dict__Property_Type_Ids__By_Ref()
        if ontology:
            for pt in ontology.property_types.values():
                if pt.property_type_id in used_type_ids:
                    property_types[pt.property_type_ref] = pt.property_type_id

        # Build filtered categories (from used node types)
        categories        = Dict__Category_Ids__By_Ref()
        used_category_ids = set()
        if ontology and taxonomy:
            for nt in ontology.node_types.values():
                if nt.node_type_ref in used_node_type_refs and nt.category_id:
                    used_category_ids.add(nt.category_id)

            # Also include ancestor categories
            all_category_ids = set(used_category_ids)
            for cat_id in used_category_ids:
                cat = taxonomy.categories.get(cat_id)
                while cat and cat.parent_id:
                    all_category_ids.add(cat.parent_id)
                    cat = taxonomy.categories.get(cat.parent_id)

            for cat_id in all_category_ids:
                cat = taxonomy.categories.get(cat_id)
                if cat:
                    categories[cat.category_ref] = cat.category_id

        return Schema__Projected__References(node_types     = node_types    ,
                                             predicates     = predicates    ,
                                             categories     = categories    ,
                                             property_names = property_names,
                                             property_types = property_types)

    # ═══════════════════════════════════════════════════════════════════════════
    # Taxonomy Section Builder
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def build_taxonomy_section(self                                 ,
                               ontology        : Schema__Ontology       ,
                               taxonomy        : Schema__Taxonomy       ,
                               projected_nodes : List__Projected__Nodes ) -> Schema__Projected__Taxonomy:
        node_type_categories = Dict__Category_Refs__By_Node_Type_Ref()
        category_parents     = Dict__Category_Refs__By_Category_Ref()

        if ontology is None or taxonomy is None:
            return Schema__Projected__Taxonomy(node_type_categories = node_type_categories,
                                               category_parents     = category_parents    )

        # Get used node type refs
        used_node_type_refs = {node.ref for node in projected_nodes if node.ref}

        # Map node types to their categories
        used_category_ids = set()
        for nt in ontology.node_types.values():
            if nt.node_type_ref in used_node_type_refs and nt.category_id:
                cat = taxonomy.categories.get(nt.category_id)
                if cat:
                    node_type_categories[nt.node_type_ref] = cat.category_ref
                    used_category_ids.add(nt.category_id)

        # Build category parent chain for all used categories and their ancestors
        categories_to_process = set(used_category_ids)
        while categories_to_process:
            cat_id = categories_to_process.pop()
            cat    = taxonomy.categories.get(cat_id)
            if cat is None:
                continue
            if cat.category_ref in category_parents:
                continue                                                             # Already processed

            if cat.parent_id:
                parent = taxonomy.categories.get(cat.parent_id)
                if parent:
                    category_parents[cat.category_ref] = parent.category_ref
                    if cat.parent_id not in used_category_ids:
                        categories_to_process.add(cat.parent_id)
                        used_category_ids.add(cat.parent_id)
            else:
                category_parents[cat.category_ref] = Category_Ref('')                # Root has empty parent

        return Schema__Projected__Taxonomy(node_type_categories = node_type_categories,
                                           category_parents     = category_parents    )

    # ═══════════════════════════════════════════════════════════════════════════
    # Sources Builder
    # ═══════════════════════════════════════════════════════════════════════════

    def build_sources(self, graph: Schema__Semantic_Graph, ontology: Schema__Ontology) -> Schema__Projected__Sources:
        ontology_seed = None                                                         # Get ontology seed if available
        if ontology and ontology.ontology_id_source:
            ontology_seed = ontology.ontology_id_source.seed

        return Schema__Projected__Sources(source_graph_id = graph.graph_id  ,
                                          ontology_seed   = ontology_seed   ,
                                          generated_at    = Timestamp_Now() )
