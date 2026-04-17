dp = {}
dp[0] = 0
dp[1] = 1
n = int(input())
for i in range(2, n+1):
    dp[i] = dp[i - 1] + dp[i - 2]
print(dp[n])

"""
n = int(input().strip())
if n < 2:
    print(n)
else:
    prev2, prev1 = 0, 1       # 分别对应 F(0), F(1)
    for _ in range(2, n + 1):
        curr = prev1 + prev2  # F(i) = F(i-1) + F(i-2)
        prev2, prev1 = prev1, curr
    print(prev1)

"""