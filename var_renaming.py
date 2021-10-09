from base_operator import BaseOperator


class VariableRenaming(BaseOperator):
    def __init__(self, language: str):
        super(VariableRenaming, self).__init__(language)
        self.var_node_types = {'identifier'}
        self.var_filter_types = {'class_declaration', 'method_declaration', 'method_invocation'}

    # Get only variable node from type "identifier"
    def get_identifier_nodes(self, tree, text):
        var_nodes, var_renames = [], {}
        queue = [tree.root_node]
        while queue:
            current_node = queue.pop(0)
            for child_node in current_node.children:
                child_type = str(child_node.type)
                if child_type in self.var_node_types:  # only identifier node
                    if str(current_node.type) in self.var_filter_types:
                        # filter out class/method name or function call identifier
                        continue
                    var_name = text[child_node.start_byte: child_node.end_byte]
                    if var_name not in var_renames:
                        var_renames[var_name] = "var{}".format(len(var_renames) + 1)
                    var_nodes.append([child_node, var_name, var_renames[var_name]])
                queue.append(child_node)
        return var_nodes

    def transform(self, id_nodes, code_text):
        id_nodes = sorted(id_nodes, reverse=True, key=lambda x: x[0].start_byte)
        for var_node, var_name, var_rename in id_nodes:
            code_text = code_text[:var_node.start_byte] + var_rename + code_text[var_node.end_byte:]
        return code_text

    def rename_variable(self, code_snippet):
        tree = self.parse(code_snippet)
        identifier_nodes = self.get_identifier_nodes(tree, code_snippet)
        return self.transform(identifier_nodes, code_snippet)
