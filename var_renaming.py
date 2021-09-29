from ast_parser import ASTParser
import tree_sitter
from tree_sitter import Node
from typing import List

# Not finished yet
class VariableRenaming()
    def __init__(self, language: str):
        super(VariableRenaming, self).__init__(language)

    # Get node with type "identifier"
    def get_identififer_nodes(self, root, text):
        queue = [root]
        var_declaration_nodes = []
        var_declarations_types = ['identifier']
        while queue:
          current_node = queue.pop(0)
          for child in current_node.children:
             child_type = str(child.type)
             if child_type in var_declarations_types:
                 var_declaration_nodes.append(child)
             queue.append(child)
        return var_declaration_nodes

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
        id_groups = {}
        for identifier_node in identifier_nodes:
            id_name = text[identifier_node.start_byte:identifier_node.end_byte]
            if id_name not in id_groups:
                id_groups[id_name] = []
            id_groups[id_name].append(identifier_node)
        return id_groups


    def transform(self, id_groups, text):

        new_t = text
        for identifier, nodes in id_groups.items():
            new_identifer = "op"

            print(identifier, "-------------")
            for n in nodes:
                print("**********")
                print(n.start_byte)
                print(n.start_point)
                print(n.end_byte)
                print(n.end_point)
                # print(text[n.start_byte:n.end_byte])
                new_t = rename_variable(n, new_t, new_identifer)
                print(new_t)
                # text[n.start_byte:n.end_byte] = new_identifer

    def rename_variable(self, code_snippet):
        tree = self.parser.parse(code_snippet)
        root_node = tree.root_node
        identifier_nodes = get_identififer_nodes(root_node, code_snippet)
        groups = group_identifier_nodes(identifier_nodes, code_snippet)
        transform(groups, code_snippet)

        # return new_text



