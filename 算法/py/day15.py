nums = list(map(int, input().split(",")))
target = int(input())
left, right = 0, len(nums) - 1
while left <= right:
    mid = (left + right) // 2
    if nums[mid] >= target:
        right = mid - 1
    else:
        left = mid + 1
print(left)