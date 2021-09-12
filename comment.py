from ast_parser import ASTParser
import tree_sitter
from tree_sitter import Node
from typing import List

def match_from_span(node: Node, lines: List) -> str:
    line_start = node.start_point[0]
    line_end = node.end_point[0]
    char_start = node.start_point[1]
    char_end = node.end_point[1]
    if line_start != line_end:
        return '\n'.join([lines[line_start][char_start:]] + lines[line_start+1:line_end] + [lines[line_end][:char_end]])
    else:
        return lines[line_start][char_start:char_end]

def delete_from_span(nodes: [Node], lines: List) -> str:
    new_lines = []
    for i in range(len(lines)):
        line_nodes = []
        for node in nodes:
            print("Start point : ", node.start_point[0])
            print("End point : ", node.end_point[0])
            line_start = node.start_point[0]
            line_end = node.end_point[0]
            char_start = node.start_point[1]
            char_end = node.end_point[1]
            if i in range(line_start,line_end+1):
                if i == line_start and i == line_end:
                    line_nodes.append([char_start, char_end])
                elif line_start == i:
                    line_nodes.append([char_start, len(lines[i])])
                elif line_end == i:
                    line_nodes.append([0, char_end])
                else:
                    line_nodes.append([0, len(lines[i])])

        # print("Line nodes")
        # print(line_nodes)
        new_line = ""
        for j in range(len(lines[i])):
            inside = False
            for s in line_nodes:
                # print(s)
                if j in range(s[0], s[1]):
                    inside = True
                    break
            if not inside:
                new_line = new_line + lines[i][j]
                print(new_line)
        new_lines.append(new_line)
    return '\n'.join(new_lines)

def get_comment_nodes(tree_splitted_code, root):
    queue = [root]
    comments = []
    comment_types = ['line_comment', 'block_comment']
    while queue:
      current_node = queue.pop(0)
      for child in current_node.children:
         child_type = str(child.type)
         if child_type in comment_types:
             comments.append(child)
         queue.append(child)
    return comments

parser = ASTParser() 
parser.set_language('rust')
code = """
    // this is a comment
    fn main() {
    /* this is another
       comment
       */
    }
"""
tree = parser.parse(bytes(code, "utf8"))
tree_splitted_code = code.split("\n")
print(tree_splitted_code)
# print(tree.root_node.sexp())
cmts = get_comment_nodes(tree_splitted_code, tree.root_node)
print(cmts)
#for child in cmts:
#    code = match_from_span(child, tree_splitted_code)
code = delete_from_span(cmts, tree_splitted_code)
tree = parser.parse(bytes(code, 'utf-8'))
print(tree.root_node.sexp())
print(code)