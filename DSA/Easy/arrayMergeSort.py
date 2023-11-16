# class Solution:
#     def mergeSort(self, arr):
#         def merge_sort(arr):
#             # low, high, n = 0, len(arr), len(arr)
#             mid = len(arr) // 2
#             left_arr = arr[:mid]
#             right_arr = arr[mid:]
#
#             left_arr = merge_sort(left_arr)
#             right_arr = merge_sort(right_arr)
#
#             return merge(self, left_arr, right_arr)
#
#         def merge(left, right):
#             merged = []
#             i = j = 0
#
#             while i < len(left) and j < len(right):
#                 if left[i] < right[j]:
#                     merged.append(left[i])
#                     i += 1
#                 else:
#                     merged.append(right[j])
#                     j += 1
#
#             merged.extend(left[i:])
#             merged.extend(right[j:])
#             print(merged)
#             return merged
#
#         merge_sort(arr)
#
#
# obj = Solution()
# arr = [5, 23, 7, 45, 29, 10, 3, 1]
# print(obj.mergeSort(arr))


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # Split the array into two halves
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # Recursively sort the two halves
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)
    print(left_half, right_half)
    # Merge the sorted halves
    return merge(left_half, right_half)

def merge(left, right):
    merged = []
    i = j = 0

    # Compare elements from the left and right halves and merge them
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append any remaining elements in the left and right halves
    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged

# Example usage
arr = [38, 27, 43, 3, 9, 82, 10]
sorted_arr = merge_sort(arr)
print(sorted_arr)
