import java.util.Scanner;

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
programming solution to find R(n) that takes input x[1,...,n],p[1,...,n] and prev[1,...,n

*/

// java code
public class correction {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();
        int[] x = new int[n];
        int[] y = new int[n];
        int[] p = new int[n];
        for (int i = 0; i < n; i++) {
            x[i] = in.nextInt();
            y[i] = in.nextInt();
            p[i] = in.nextInt();
        }
        int[] prev = new int[n];
        int[] next = new int[n];
        for (int i = 0; i < n; i++) {
            prev[i] = -1;
            next[i] = -1;
        }
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (x[j] < x[i] - 3) {
                    prev[i] = j;
                    break;
                }
            }
        }
        for (int i = n - 1; i >= 0; i--) {
            for (int j = n - 1; j > i; j--) {
                if (x[j] > x[i] + 3) {
                    next[i] = j;
                    break;
                }
            }
        }
        int[][] dp = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                dp[i][j] = -1;
            }
        }
        for (int i = 0; i < n; i++) {
            dp[i][i] = p[i];
        }
        for (int l = 2; l <= n; l++) {
            for (int i = 0; i <= n - l; i++) {
                int j = i + l - 1;
                dp[i][j] = Integer.MIN_VALUE;
                for (int k = i; k <= j; k++) {
                    dp[i][j] = Math.max(dp[i][j], dp[i][k - 1] + dp[k + 1][j] + y[i - 1] * y[j + 1]);
                }
            }
        }
        System.out.println(dp[0][n - 1]);
    }
}
