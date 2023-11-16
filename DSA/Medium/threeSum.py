class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        result = []
        nums.sort()

        for i,a  in enumerate(nums):
            if i > 0 and a == nums[i-1]:
                continue
            start, end = i+1, len(nums) - 1
            while start < end:
                current_sum = nums[i] + nums[start] + nums[end]

                if current_sum > 0:
                    end -= 1
                elif current_sum < 0:
                    start += 1
                else:
                    result.append([nums[i], nums[start], nums[end]])
                    start += 1
                    while nums[start] == nums[start-1] and start < end:
                        start += 1
        return result


obj = Solution()
nums = [-1,0,1,2,-1,-4]
print(obj.threeSum(nums))