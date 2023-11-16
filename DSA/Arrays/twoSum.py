class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        # result = []
        # n = len(nums)
        # left, right = 0, n-1
        # while left < right:
        #     current_sum = nums[left] + nums[right]
        #     if current_sum == target:
        #         result.append([left,right])
        #         # # left += 1
        #         # right -= 1
        #     elif current_sum < target:
        #         left += 1
        #     else:
        #         right -= 1
        #
        # return result
        num_dict = {}  # Dictionary to store elements and their indices
        result = []

        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_dict:
                # return [num_dict[complement], i]
                result.append([num_dict[complement], i])
            num_dict[num] = i

        # No solution found
        return result


obj = Solution()
nums = [2,7,11,15,8,1]
target = 9
print(obj.twoSum(nums,target))