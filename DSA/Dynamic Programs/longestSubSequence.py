class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        result = []
        n = len(nums)
        result = [1] * n
        for i in range(n-1,-1,-1):
                for j in range(i+1, n):
                    if nums[i] < nums[j]:
                      result[i] = max(result[i], result[j]+1)
        return max(result)

obj = Solution()
nums = [10,9,2,5,3,10,6,7,8,101,18]
print(obj.lengthOfLIS(nums))