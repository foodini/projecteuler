#include <stdio.h>

int main()
{
    int count=0;
    for (int cc=0; cc<=200;               cc+=200)
    for (int c=0;  cc+c<=200;             c+=100)
    for (int l=0;  cc+c+l<=200;           l+=50)
    for (int xx=0; cc+c+l+xx<=200;        xx+=20)
    for (int x=0;  cc+c+l+xx+x<=200;      x+=10)
    for (int v=0;  cc+c+l+xx+x+v<=200;    v+=5)
    for (int ii=0; cc+c+l+xx+x+v+ii<=200; ii+=2)
    {
        count++;
    }
    printf("%d\n", count);
}
