#!/usr/bin/env python3
"""
快速排序算法 - 简化版本
"""


def quick_sort(arr):
    """快速排序 - 返回新列表"""
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


def quick_sort_inplace(arr):
    """快速排序 - 原地排序"""
    def _quick_sort(arr, low, high):
        if low < high:
            pivot = partition(arr, low, high)
            _quick_sort(arr, low, pivot - 1)
            _quick_sort(arr, pivot + 1, high)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    _quick_sort(arr, 0, len(arr) - 1)


# 测试代码
if __name__ == "__main__":
    # 测试数据
    test_data = [64, 34, 25, 12, 22, 11, 90]

    print("原始数组:", test_data)

    # 使用函数式排序
    sorted_data = quick_sort(test_data)
    print("函数式排序结果:", sorted_data)

    # 使用原地排序
    data_copy = test_data.copy()
    quick_sort_inplace(data_copy)
    print("原地排序结果:", data_copy)

    # 验证排序正确性
    assert sorted_data == sorted(test_data)
    assert data_copy == sorted(test_data)
    print("测试通过！")
