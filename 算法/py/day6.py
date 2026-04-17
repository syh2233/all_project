def find_min(nums):
    # 边界：如果只有一个元素，直接返回
    if len(nums) == 1:
        return nums[0]

    # 定义左右指针
    left = 0
    right = len(nums) - 1

    # 如果数组根本没被旋转（纯升序），最小值就是第一个
    # 例如 [1,2,3,4]：首元素 <= 尾元素
    if nums[left] <= nums[right]:
        return nums[left]

    # 进入二分循环：每次缩小一半搜索区间
    while left < right:
        mid = (left + right) // 2

        # 观察中点和右端的关系，决定往哪边缩
        # 画图理解：右半段如果“乱”了，最小值在右边；否则在左边（含mid）
        # 情况1：nums[mid] > nums[right]，说明最小值在右侧（不含mid）
        if nums[mid] > nums[right]:
            # TODO: 把 left 移到 mid 的右边
            # left =  ???
            pass
        else:
            # 情况2：nums[mid] <= nums[right]，最小值在左侧（包含mid）
            # TODO: 把 right 移到 mid 的位置（因为 mid 也可能是最小值）
            # right = ???
            pass

    # 循环结束时，left == right 指向最小值
    return nums[left]
