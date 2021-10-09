import config as cf
from var_renaming import VariableRenaming


def main():
    var_renaming_operator = VariableRenaming(language=cf.JAVA_LANGUAGE)

    sample_code = """
        public class Main {
          public static void main(String[] args) {
            int a = 15;
            int b = 20;
            int c = a + f(b);
          }
        }
    """

    var_renaming_code = var_renaming_operator.rename_variable(sample_code)
    print(var_renaming_code)


if __name__ == "__main__":
    main()
