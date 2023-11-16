class Solution:
    def missingNumber(self, nums: list[int]) -> int:
        result = 0
        n = len(nums)
        total_sum = n *(n+1) //2
        current_sum = sum(nums)
        result = total_sum - current_sum
        return result


obj = Solution()
nums = [0, 1, 2, 3, 6, 5]
print(obj.missingNumber(nums))