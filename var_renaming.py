from tree_sitter import Parser


# In Progress
class VariableRenaming:
    def __init__(self, language):
        self.parser = Parser()
        self.parser.set_language(language)

    # Get node with type "identifier"
    def get_identifier_nodes(self, root, text):
        queue = [root]
        var_nodes = []
        var_node_types = {'identifier'}
        var_parent_types = {'parameter', 'argument', 'variable', 'expression'}
        while queue:
            current_node = queue.pop(0)
            for child in current_node.children:
                child_type = str(child.type)
                if child_type in var_node_types:  # only identifier node
                    parent_type = str(current_node.type)
                    # filter out class/method name or function call identifier
                    if any(type_ in parent_type for type_ in var_parent_types):
                        var_nodes.append(child)
                queue.append(child)
        return var_nodes

    """
    Group nodes that has the same identifier into the same group
    E.g., 
    {
        "a": [Nodes, Nodes],
        "b": [Nodes],
        "c": [Nodes]
    }
    """

    def group_identifier_nodes(self, identifier_nodes, text):
        id_list, id_dct = [], {}
        for identifier_node in identifier_nodes:
            id_name = text[identifier_node.start_byte:identifier_node.end_byte]
            id_point = (identifier_node.start_byte, identifier_node.end_byte)
            id_dct[id_name] = id_dct[id_name] if id_name in id_dct else "var{}".format(len(id_dct) + 1)
            id_list.append([id_point, id_name, id_dct[id_name]])
        return id_list

    def transform(self, id_groups, text):
        text_list = list(text)
        id_groups = sorted(id_groups, reverse=True, key=lambda x: x[0])
        for point, name, rename in id_groups:
            text_list[:] = text_list[:point[0]] + list(rename) + text_list[point[1]:]
        return ''.join(text_list)

    def rename_variable(self, code_snippet):
        tree = self.parser.parse(bytes(code_snippet, "utf8"))
        root_node = tree.root_node
        identifier_nodes = self.get_identifier_nodes(root_node, code_snippet)
        identifier_groups = self.group_identifier_nodes(identifier_nodes, code_snippet)
        renamed_code_snippet = self.transform(identifier_groups, code_snippet)
        return renamed_code_snippet
