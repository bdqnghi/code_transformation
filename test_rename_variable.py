import sys
from var_renaming import VariableRenaming

def main():
    
    var_renaming_operator = VariableRenaming(language="java")

    sample_code = """
        public class Main {
          public static void main(String[] args) {
            int a = 15;
            int b = 20;
            int c = a + b;
          }
        }
    """

   

if __name__ == "__main__":
    main()
