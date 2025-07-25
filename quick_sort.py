#!/usr/bin/env python3
"""
快速排序算法实现
包含两种实现方式：
1. 函数式实现（返回新列表）
2. 原地排序实现（修改原列表）
"""


def quick_sort(arr):
    """
    快速排序主函数 - 函数式实现

    参数:
        arr: 待排序的列表

    返回:
        排序后的新列表
    """
    if len(arr) <= 1:
        return arr

    # 选择基准值（这里选择中间元素）
    pivot = arr[len(arr) // 2]

    # 分区操作
    left = [x for x in arr if x < pivot]      # 小于基准值的元素
    middle = [x for x in arr if x == pivot]   # 等于基准值的元素
    right = [x for x in arr if x > pivot]     # 大于基准值的元素

    # 递归排序左右两部分并合并结果
    return quick_sort(left) + middle + quick_sort(right)


def quick_sort_inplace(arr, low=0, high=None):
    """
    原地快速排序（不创建新列表）

    参数:
        arr: 待排序的列表
        low: 起始索引（默认0）
        high: 结束索引（默认len(arr)-1）
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        # 分区操作，返回基准值的最终位置
        pivot_index = partition(arr, low, high)

        # 递归排序基准值左右两部分
        quick_sort_inplace(arr, low, pivot_index - 1)
        quick_sort_inplace(arr, pivot_index + 1, high)


def partition(arr, low, high):
    """
    分区操作，将数组分为两部分

    参数:
        arr: 待分区的列表
        low: 起始索引
        high: 结束索引

    返回:
        基准值的最终位置索引
    """
    # 选择最右边的元素作为基准值
    pivot = arr[high]

    # i指向小于基准值的区域的最后一个元素
    i = low - 1

    # 遍历数组，将小于基准值的元素移到左边
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # 将基准值放到正确的位置
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def test_quick_sort():
    """测试快速排序函数"""
    # 测试用例
    test_cases = [
        [3, 6, 8, 10, 1, 2, 1],
        [5, 2, 9, 1, 5, 6],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [1],
        [],
        [3, 3, 3, 3],
        [-1, 5, -3, 0, 2, -8]
    ]

    print("测试快速排序算法:")
    print("=" * 50)

    for i, test_case in enumerate(test_cases, 1):
        original = test_case.copy()

        # 测试非原地排序
        sorted_result = quick_sort(test_case)
        print(f"测试 {i}:")
        print(f"  原始数组: {original}")
        print(f"  排序结果: {sorted_result}")

        # 测试原地排序
        test_case_copy = original.copy()
        quick_sort_inplace(test_case_copy)
        print(f"  原地排序: {test_case_copy}")
        print()


if __name__ == "__main__":
    test_quick_sort()

    # 用户交互示例
    print("自定义测试:")
    try:
        user_input = input("请输入要排序的数字，用空格分隔: ")
        numbers = list(map(int, user_input.split()))

        print(f"\n原始数组: {numbers}")

        # 使用非原地排序
        sorted_numbers = quick_sort(numbers)
        print(f"排序结果: {sorted_numbers}")

        # 使用原地排序
        numbers_copy = numbers.copy()
        quick_sort_inplace(numbers_copy)
        print(f"原地排序: {numbers_copy}")

    except ValueError:
        print("请输入有效的整数！")
    except KeyboardInterrupt:
        print("\n程序已退出")
