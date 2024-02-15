from osbot_utils.utils.Dev import pprint


class Trace_Call__View_Model:

    def __init__(self):
        self.view_model = []

    def create(self, stack):
        root_node = stack.root_node
        if root_node:
            target = [root_node]
            self.view_model = self.create_view_model(target)
            self.fix_view_mode()                                        # Fix the view mode for the last node
        return self.view_model

    # todo: rename view_model so that it is not confused with self.view_model
    def create_view_model(self, json_list, level=0, prefix="", view_model=None):
        if view_model is None:
            view_model = []                                                                 # Initialize view model if None
        for idx, node in enumerate(json_list):                                              # Iterate over each node in the JSON list to populate the view model
            components           = node.name.split('.')
            duration             = node.call_duration
            extra_data           = node.extra_data
            frame_locals         = node.locals
            lines                = node.lines
            source_code          = node.source_code
            source_code_caller   = node.source_code_caller
            source_code_location = node.source_code_location
            method_name          = components[-1]
            if len(components) > 1:
                method_parent  = f"{components[-2]}"
            else:
                method_parent  = ""
            if method_name == "__init__":                                                   # Adjust the method_name based on special method names like __init__ and __call__
                method_name = f"{method_parent}.{method_name}"
            elif method_name == "__call__":
                method_name = f"{method_parent}.{method_name}"
            elif method_name == "<module>":
                method_name = f"{method_parent}.{method_name}"

            pruned_parents = [comp for comp in components]
            parent_info = '.'.join(pruned_parents[:-1])

            if level == 0:                                                                  # Handle tree representation at level 0
                emoji = "📦 "
                tree_branch = ""
            else:
                is_last_sibling = (idx == len(json_list) - 1)                               # Check if the node is the last sibling
                tree_branch = "└── " if is_last_sibling else "├── "
                emoji = "🧩️" if not node.children else "🔗️"

            view_model.append({ 'duration'            : duration             ,
                                'emoji'               : emoji                ,
                                'extra_data'          : extra_data           ,
                                'method_name'         : method_name          ,
                                'method_parent'       : method_parent        ,
                                'lines'               : lines                ,
                                'locals'              : frame_locals         ,  # todo finish refactoring use of locals to frame_locals
                                'parent_info'         : parent_info          ,
                                'prefix'              : prefix               ,
                                'source_code'         : source_code          ,
                                'source_code_caller'  : source_code_caller   ,
                                'source_code_location': source_code_location ,
                                'tree_branch'         : tree_branch          ,})
            next_prefix = prefix + ("    " if tree_branch == "└── " else "│   ")            # Calculate the prefix for the next level
            self.create_view_model(node.children, level + 1, prefix=next_prefix, view_model=view_model)

        return view_model

    def fix_view_mode(self):
        if len(self.view_model) > 0:                                                        # these changes will provide a nice end of tree, for example replacing "│       ├──" with "└────────── "
            last_node = self.view_model[-1]                                                 # Get the last node in the view model
            last_node['prefix'] = last_node['prefix'].replace(' ', '─').replace('│', '└')   # Update the prefix for the last node
            last_node['tree_branch'] = '─── '
