from ast_parser import ASTParser
import tree_sitter
from tree_sitter import Node
from typing import List


# Get node with type "identifier"
def get_identififer_nodes(root, text):
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
def group_identifier_nodes(identifier_nodes, text):
    id_groups = {}
    for identifier_node in identifier_nodes:
        id_name = text[identifier_node.start_byte:identifier_node.end_byte]
        if id_name not in id_groups:
            id_groups[id_name] = []
        id_groups[id_name].append(identifier_node)
    return id_groups


def transform(id_groups, text):

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

def rename_variable(identifier_node, text, new_name):
    lines = text.split("\n")
    # var_belong_to_line = identifier_node.start_point[0]
    # print("Line : ", var_belong_to_line)
    new_text = text[0:identifier_node.start_byte]
    # print("N : ", new_text)
    # print("########")
    new_text = new_text + new_name
    new_text = new_text + text[identifier_node.end_byte:len(text)-1]
    return new_text


parser = ASTParser() 
parser.set_language('java')
text = """
public class Main {
  public static void main(String[] args) {
    int a = 15;
    int b = 20;
    int c = a + b;
  }
}

"""
tree = parser.parse(bytes(text, encoding='utf8'))

root_node = tree.root_node
print(root_node.sexp())

identifier_nodes = get_identififer_nodes(root_node, text)
print(identifier_nodes)

groups = group_identifier_nodes(identifier_nodes, text)
# print(groups)
transform(groups, text)
