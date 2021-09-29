import sys
from comment_deletion import CommentDeletion

def main():
    
    comment_deletion_operator = CommentDeletion(language="rust")

    code_with_comment = """
    // this is a comment
    fn main() {
    /* this is another
       comment
       */
    }
    """

    code_without_comment = comment_deletion_operator.delete_comments(code_with_comment)
    print(code_without_comment)

if __name__ == "__main__":
    main()
