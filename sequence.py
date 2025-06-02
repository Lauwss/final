def max_subarray_sum(arr):
    if not arr:
        return 0
    current_max = global_max = arr[0]
    for num in arr[1:]:
        current_max = max(num, current_max + num)
        global_max = max(global_max, current_max)
    return global_max

test_cases = [
    [1, -2, 3, 5, -1],    # 预期输出: 8 (子数组 [3, 5])
    [1, -2, 3, -8, 5, 1], # 预期输出: 6 (子数组 [5, 1])
    [1, -2, 3, -2, 5, 1], # 预期输出: 7 (子数组 [3, -2, 5, 1])
    [-2, -3, -1],         # 预期输出: -1 (子数组 [-1])
    [5, 4, -1, 7, 8],     # 预期输出: 23 (整个数组)
    []                    # 预期输出: 0 (空数组)
]

# 执行测试
for i, arr in enumerate(test_cases, 1):
    result = max_subarray_sum(arr)
    print(f"测试用例 {i}: 数组 = {arr}")
    print(f"最大子数组和: {result}")
    print("-" * 40)    