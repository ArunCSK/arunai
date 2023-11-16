class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        def max_crossing_sum(nums, low, mid, high):
            left_sum = float('-inf')
            current_sum = 0

            # Calculate the maximum sum in the left half
            for i in range(mid, low - 1, -1):
                current_sum += nums[i]
                left_sum = max(left_sum, current_sum)

            right_sum = float('-inf')
            current_sum = 0

            # Calculate the maximum sum in the right half
            for i in range(mid + 1, high + 1):
                current_sum += nums[i]
                right_sum = max(right_sum, current_sum)

            # Return the sum of the maximum subarrays in the left and right halves
            return left_sum + right_sum

        def max_subarray_sum_divide_conquer(nums, low, high):
            if low == high:
                return nums[low]

            mid = (low + high) // 2

            # Recursively find the maximum subarray sum in the left and right halves
            left_sum = max_subarray_sum_divide_conquer(nums, low, mid)
            right_sum = max_subarray_sum_divide_conquer(nums, mid + 1, high)
            print(left_sum, right_sum)
            # Find the maximum subarray sum that crosses the midpoint
            cross_sum = max_crossing_sum(nums, low, mid, high)

            # Return the maximum of the three sums
            return max(left_sum, right_sum, cross_sum)

        # Wrapper function for easier usage
        def max_subarray_sum(nums):
            return max_subarray_sum_divide_conquer(nums, 0, len(nums) - 1)

        return max_subarray_sum(nums)

# Example usage
obj = Solution()
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
result = obj.maxSubArray(nums)
print(result)  # Output: 6
