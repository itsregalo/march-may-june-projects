
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