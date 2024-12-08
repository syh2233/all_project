n, m = map(int, input().split())
arr = []
for _ in range(n):
    arr.append(list(input().split(" ")))
max_sum = float('-inf')
for x1 in range(n-1):
    for y1 in range(m-1):
        L=min(n-x1,m-y1)
        for l in range(1,L):
            x2 = x1 + l
            y2 = y1 + l
        s = 0
        for x in range(x1, x2 + 1):
            s+=int(arr[x][y1])
        for y in range(y1, y2 + 1):
            s+=int(arr[x1][y])
        for x in range(x1, x2 + 1):
            s+=int(arr[x][y2])
        for y in range(y1, y2 + 1):
            s+=int(arr[x2][y])
        s-=int(arr[x1][y1])
        s-=int(arr[x1][y2])
        s-=int(arr[x2][y1])
        s-=int(arr[x2][y2])
        max_sum= max(max_sum,s)
        
print(max_sum)
