class Solution:
    def findMin(self, nums: list[int]) -> int:
        return min(nums)


obj = Solution()
nums = [3,4,5,1,2]
print(obj.findMin(nums))