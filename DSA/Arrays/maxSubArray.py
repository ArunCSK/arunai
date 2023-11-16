class Solution:
    def maxSubArray(self, nums: list[int]) -> int:

        n = len(nums)
        max_sum = nums[0]
        current_sum = nums[0]

        for i in range(1,n):
            current_sum = max(nums[i], current_sum + nums[i])
            max_sum = max(max_sum, current_sum)

        return max_sum

obj = Solution()
nums = [-2,1,-3,4,-1,2,1,-5,4]
print(obj.maxSubArray(nums))