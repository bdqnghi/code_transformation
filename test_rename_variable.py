from var_renaming import VariableRenaming


def main():
    var_renaming_operator = VariableRenaming(language="java")

    sample_codes = [
        """
        public class Main {
          public static void main(String[] args) {
            int a = 15;
            int b = 20;
            int c = a + f(b);
          }
        }
        """,
        """
        void bubbleSort(int arr[], int n)
        {
           int i, j;
           for (i = 0; i < n-1; i++)     
         
               // Last i elements are already in place  
               for (j = 0; j < n-i-1; j++)
                   if (arr[j] > arr[j+1])
                      swap(&arr[j], &arr[j+1]);
        }
        """
    ]

    for sample_code in sample_codes:
        var_renaming_code = var_renaming_operator.rename_variable(sample_code)
        print(var_renaming_code)
        print("-" * 50)


if __name__ == "__main__":
    main()
