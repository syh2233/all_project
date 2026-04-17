n = int(input())
if n <= 2:
    print(n)
else:
    prev2,prev1 = 1,2
    for _ in range(3,n+1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr