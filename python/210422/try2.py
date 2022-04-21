"""
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
programming solution to find R(n) that takes input x[1,...,n],p[1,...,n] and prev[1,...,
"""

def main():
    n = int(input())
    x = [int(i) for i in input().split()]
    y = [int(i) for i in input().split()]
    p = [int(i) for i in input().split()]
    prev = [0] * n
    next = [0] * n
    for i in range(n):
        if i == 0:
            prev[i] = 0
        else:
            prev[i] = max(prev[i - 1], x[i - 1] - 3)
    for i in range(n - 1, -1, -1):
        if i == n - 1:
            next[i] = n
        else:
            next[i] = min(next[i + 1], x[i + 1] + 3)
    revenue = [0] * n
    for i in range(n):
        revenue[i] = p[i]
        for j in range(prev[i], i):
            if x[j] < x[i] - 3:
                revenue[i] = max(revenue[i], revenue[j] + p[i])
        for j in range(i + 1, next[i]):
            if x[j] > x[i] + 3:
                revenue[i] = max(revenue[i], revenue[j] + p[i])
    print(max(revenue))

main()