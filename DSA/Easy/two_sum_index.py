class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        num_dict = {}  # Dictionary to store numbers and their indices

        for i, num in enumerate(nums):
            # print(i, num)
            complement = target - num
            print(complement)
            if complement in num_dict:
                print(num_dict)
                return [num_dict[complement], i]
            num_dict[num] = i

        return None  # If no such pair is found


obj = Solution()
nums = [3, 2, 3]
target = 6
print(obj.twoSum(nums, target))
