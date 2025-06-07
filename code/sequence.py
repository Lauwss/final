"""
该模块用于计算数组的最大子数组和，并通过一系列测试用例验证计算函数的正确性。
包含一个核心函数 max_subarray_sum 用于实现最大子数组和的计算逻辑，
以及对该函数进行测试的相关代码。
"""

def max_subarray_sum(arr):
    """
    计算给定数组的最大子数组和。

    Args:
        arr (list): 输入的整数数组，可能为空。

    Returns:
        int: 数组的最大子数组和，如果数组为空则返回 0。
    """
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

for i, test_array in enumerate(test_cases, 1):
    result = max_subarray_sum(test_array)
    print(f"测试用例 {i}: 数组 = {test_array}")
    print(f"最大子数组和: {result}")
    print("-" * 40)
    