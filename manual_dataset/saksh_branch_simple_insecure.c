#include <stdio.h> 
int main(void) {     
  int result = 1;
  if ((result > 1) || (result < 3)) {
    if (result < 3) {
      printf("Executing critical code...\n");
      }
    }
    else {
      printf("Exiting out...\n");
      return 1;
      }
  return 0;
}

              