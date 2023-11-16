class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        # result = []
        # n = len(nums)
        # for i in range(n):
        #     for j in range(n-i):
        #         print(nums[j+i])
        #
        # return  result
        n = len(nums)
        result = [1] * n
        prefix = 1
        for i in range(n):
            result[i] = prefix
            prefix *= nums[i]
        postfix = 1
        for i in range(n-1, -1, -1):
            result[i] *= postfix
            postfix *= nums[i]
        return result



obj = Solution()
nums = [1,2,3,4]
print(obj.productExceptSelf(nums))