height = list(map(int, input().split(",")))
left, right = 0, len(height) - 1
ans = 0
while left < right:
        # 当前容器的面积
        area = (right - left) * min(height[left], height[right])
        ans = max(ans, area)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1