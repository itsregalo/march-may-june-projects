
#include <iostream>
#include <cmath>
using namespace std;

/*
Suppose you are managing construction of billboards on the 21st St. N.
which runs from east to west on a straight line. There are n possible sites for billboard construction
given in the array x[1,...,n], where 0 ≤ x[1] < x[2] < ··· < x[n] specifies the distance of each possible
billboard location from the west side end of 21st St. N. There is also an array p[1,...n] containing
the payment information, i.e., if you place a billboard at location x[j] you receive payment p[j].
Restrictions imposed by the Sedgwick county requires that any pair of billboard must be more than
3 miles apart. You would like place the billboard at a subset of sites so as to maximize your
revenue, subject to Sedgwick county’s placement restriction. For example, if n = 4, x = [3,4,8,9]
and p = [5,6,5,1] then optimal solution will place billboards at x[2] and x[3] with revenue p[2] +
p[3] = 6 + 5 = 11.
Suppose you are also given the array prev[1,...,n] where prev[j] stores the location index of the
previous billboard site (to the west of x[j]) that satisfies Sedgwick county’s billboard restriction.
If no such location exists the prev[j] = 0, otherwise, prev[j] = max{i : i < j and x[i] < x[j] − 3}. Let
R(j) denote the optimal revenue obtained by placing billboards at a subset of locations
x[1],x[2],...,x[j] satisfying Sedgwick county’s restriction. Then our goal is to find R(n). First, write
R(j) in terms of solution of smaller subproblem (optimal substructure) and give a dynamic
programming solution to find R(n) that takes input x[1,...,n],p[1,...,n] and prev[1,...,n]. What is the
running time of your solution? For convenience assume prev[1] = 0 and R(0) = 0
*/

// solution 1:
// time complexity: O(n^2)
// space complexity: O(n)

// function to find the optimal solution

/*
Example
Input:
x = [3,4,8,9]
p = [5,6,5,1]
prev = [0,1,2,3]
Output:
11
*/

// function to find the optimal solution
int find_optimal_solution(int x[], int p[], int prev[], int n)
{
    int R[n+1];
    R[0]=0;
    for(int i=1;i<=n;i++)
    {
        R[i]=p[i];
        for(int j=1;j<i;j++)
        {
            if(x[j]<x[i]-3)
            {
                R[i]=max(R[i],R[j]+p[i]);
            }
        }
    }
    return R[n];
}

// main function
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

    int prev[n+1];
    prev[0]=0;
    for(int i=1;i<=n;i++)
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
    cout << "The optimal solution is: " << find_optimal_solution(x,p,prev,n) << endl;
    return 0;
}