
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int equal(char, char);

// minimum of two values
long min2(size_t a, size_t b)
{
    if (a < b)
    {
        return a;
    }
    return b;
}

// minimum of three values
long min3(size_t a, size_t b, size_t c)
{
    return min2(a, min2(b, c) ) ;
}

int
main(int argc, char **argv) {
    int **Matrix;
    int i, j;

    int needle_len = strlen(argv[1]);
    int haystack_len = strlen(argv[2]);

    char* needle_str = argv[1];
    char* haystack_str = argv[2];

    printf("%d\n", needle_len);
    printf("%s\n", needle_str);
    printf("%d\n",haystack_len);
    printf("%s\n", haystack_str);

    Matrix = (int **) malloc((needle_len+1)*sizeof(int*));
    for(i=0; i<=needle_len; i++)
        Matrix[i] = (int*) malloc((haystack_len+1)*sizeof(int));    

    for( i=0 ; i<=needle_len ; i++ )   Matrix[i][0] = i;
        
    for( j=0 ; j<=haystack_len ; j++ ) {
        if(j==0 || haystack_str[j-1] == ' ')      
            Matrix[0][j] = 0;
        else
            Matrix[0][j] = Matrix[0][j-1] + 1;
    }
    
    for( i=1 ; i<=needle_len ; i++ )
        for( j=1 ; j<=haystack_len ; j++ )
            Matrix[i][j] = min3(
                Matrix[i-1][j] + 1,
                Matrix[i][j-1] + 1,
                Matrix[i-1][j-1] + equal(haystack_str[j-1], needle_str[i-1]));

    for( i=0 ; i<=needle_len ; i++ ) {
        for( j=0 ; j<=haystack_len ; j++ ) {
            printf("%d ", Matrix[i][j]);
        }
        printf("\n");
    }


    // return min(row1)
    long min_cost = needle_len;
    for (i = 1; i <= haystack_len; ++i)
    {   
        if (Matrix[needle_len][i] < min_cost)
        {
            min_cost = Matrix[needle_len][i];
        }
    }

    printf("\n");

    return 0;
}

int equal(char x, char y) {
    if(x==y)
        return 0;
    return 1;
}