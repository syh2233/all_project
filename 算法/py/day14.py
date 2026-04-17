nums = list(map(int,input().split(",")))
k = int(input())
count = 0
nums.append(0)
for i in range(len(nums)-1):
    if nums[i]+nums[i+1] == k:
        count += 1
print(count)