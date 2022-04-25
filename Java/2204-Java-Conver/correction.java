import java.util.Scanner;

public class correction {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] x = new int[n];
        int[] p = new int[n];
        int[] prev = new int[n];
        for (int i = 0; i < n; i++) {
            x[i] = sc.nextInt();
            p[i] = sc.nextInt();
        }
        prev[0] = 0;
        for (int i = 1; i < n; i++) {
            int max = 0;
            for (int j = 0; j < i; j++) {
                if (x[j] < x[i] - 3) {
                    if (max < p[j] + p[i]) {
                        max = p[j] + p[i];
                        prev[i] = j;
                    }
                }
            }
        }
        int max = 0;
        for (int i = 0; i < n; i++) {
            if (max < p[i] + p[prev[i]]) {
                max = p[i] + p[prev[i]];
            }
        } 
        System.out.println(max-2);
    }
}

