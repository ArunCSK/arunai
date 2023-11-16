from collections import Counter
import heapq


def topKFrequent(nums, k):
    # Use Counter to get the frequency of each element
    counter = Counter(nums)
    # print(counter)
    # Use a min-heap to keep track of the k most frequent elements
    heap = [(-freq, num) for num, freq in counter.items()]
    heapq.heapify(heap)
    print(heap)

    # Extract the k most frequent elements from the heap
    result = []
    for _ in range(k):
        result.append(heapq.heappop(heap)[1])

    return result


# Example usage
nums1 = [1, 1, 1, 2, 2, 3]
k1 = 2
result1 = topKFrequent(nums1, k1)
# print(result1)  # Output: [1, 2]

# nums2 = [3,0,1,0]
# k2 = 1
# result2 = topKFrequent(nums2, k2)
# print(result2)  # Output: [1]
