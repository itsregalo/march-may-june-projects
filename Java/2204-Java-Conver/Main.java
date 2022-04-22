import java.util.Scanner;

class Main {
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
                for ( int k = i; k <= j; k++) {
                    dp[i][j] = Math.max(dp[i][j], dp[i][k] + dp[k + 1][j]);
                }
                if (prev[i] != -1) {
                    dp[i][j] = Math.max(dp[i][j], dp[prev[i]][j] + p[i]);
                }
                if (next[j] != -1) {
                    dp[i][j] = Math.max(dp[i][j], dp[i][next[j]] + p[j]);
                }
            }
        }
        System.out.println(dp[0][n - 1]);
    }
}