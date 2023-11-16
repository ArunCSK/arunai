class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)

        # Initialize the result array with 1s
        result = [1] * n

        # Calculate the prefix products
        prefix_product = 1
        for i in range(n):
            result[i] *= prefix_product
            prefix_product *= nums[i]

        # Calculate the suffix products and update the result
        suffix_product = 1
        for i in range(n - 1, -1, -1):
            result[i] *= suffix_product
            suffix_product *= nums[i]

        return result


obj = Solution()
nums = [1,2,3,4,5,6]
print(obj.productExceptSelf(nums))