#include <iostream>
#include <cmath>
using namespace std;

int main()
{
    int n;
    cout << "Please enter n: ";
    cin>>n;
    int x[n+1],p[n+1];

    for(int i=1;i<=n;i++)
    {
        cout << "Please enter x: ";
        cin>>x[i];
    }
    
    for(int i=1;i<=n;i++)
    {
        cout << "Please enter p: ";
        cin>>p[i];
    }

    int prev[n+1],next[n+1];
    prev[1]=1;

    for(int i=2;i<=n;i++)
    {
        prev[i]=i;
        for(int j=1;j<i;j++)
        {
            if(x[j]<x[i]-3)
            {
                prev[i]=j;
                break;
            }
        }
    }
    
    next[n]=n;
    for(int i=n-1;i>=1;i--)
    {
        next[i]=i;
        for(int j=n;j>i;j--)
        {
            if(x[j]>x[i]+3)
            {
                next[i]=j;
                break;
            }
        }
    }
    int R[n+1];
    R[1]=p[1];
    for(int i=2;i<=n;i++)
    {
        R[i]=R[prev[i]]+p[i];
    }
    for(int i=n-1;i>=1;i--)
    {
        R[i]=max(R[next[i]],R[i]);
    }
    cout<<"R(n) = "<<R[n]<<endl;
    return 0;
}