# ═══════════════════════════════════════════════════════════════════════════════
# Call Flow Storage - Load and save call flow graphs to the file system
# Uses Type_Safe .json() and .from_json() for serialization
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                          import Optional
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Flow__Result          import Schema__Call_Flow__Result
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.utils.Json                                                          import json_load_file, json_save_file_pretty
from osbot_utils.utils.Files                                                         import file_exists, folder_create, parent_folder, file_delete
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph        import Schema__Semantic_Graph

class Call_Flow__Storage(Type_Safe):                                                 # Load and save call flow graphs
    base_path : str = ''                                                             # Base path for storage

    # ═══════════════════════════════════════════════════════════════════════════
    # Save Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def save(self                                                                    ,
             result    : Schema__Call_Flow__Result                                   ,
             file_path : str                                                         ) -> bool:
        try:                                                                         # Save result to JSON file
            folder_create(parent_folder(file_path))
            json_save_file_pretty(result.json(), file_path)
            return True
        except Exception as e:
            print(f"Error saving call flow: {e}")
            return False

    def save_graph_only(self                                                         ,
                        graph     : Schema__Semantic_Graph                           ,
                        file_path : str                                              ) -> bool:
        try:                                                                         # Save only the graph (no metadata)
            folder_create(parent_folder(file_path))
            json_save_file_pretty(graph.json(), file_path)
            return True
        except Exception as e:
            print(f"Error saving graph: {e}")
            return False

    # ═══════════════════════════════════════════════════════════════════════════
    # Load Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def load(self, file_path: str) -> Optional[Schema__Call_Flow__Result]:           # Load result from JSON file
        if not file_exists(file_path):
            return None
        try:
            data = json_load_file(file_path)
            return Schema__Call_Flow__Result.from_json(data)
        except Exception as e:
            print(f"Error loading call flow: {e}")
            return None

    def load_graph_only(self, file_path: str) -> Optional[Schema__Semantic_Graph]:   # Load only the graph (no metadata)
        if not file_exists(file_path):
            return None
        try:
            data = json_load_file(file_path)
            return Schema__Semantic_Graph.from_json(data)
        except Exception as e:
            print(f"Error loading graph: {e}")
            return None

    # ═══════════════════════════════════════════════════════════════════════════
    # Delete Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def delete(self, file_path: str) -> bool:                                        # Delete a saved file
        return file_delete(file_path)

    def exists(self, file_path: str) -> bool:                                        # Check if file exists
        return file_exists(file_path)

    # ═══════════════════════════════════════════════════════════════════════════
    # String Serialization
    # ═══════════════════════════════════════════════════════════════════════════

    def to_json(self, result: Schema__Call_Flow__Result) -> str:                     # Serialize result to JSON string
        import json
        return json.dumps(result.json(), indent=2)

    def from_json(self, json_str: str) -> Schema__Call_Flow__Result:                 # Deserialize result from JSON string
        import json
        data = json.loads(json_str)
        return Schema__Call_Flow__Result.from_json(data)
