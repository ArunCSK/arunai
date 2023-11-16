class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        result = []
        n = len(nums)
        nums.sort()

        for i,a in enumerate(nums):
            if i > 0 and a == nums[i-1]:
                continue

            left, right = i+1, n-1
            while left < right:
                threeSum = nums[i] + nums[right] + nums[left]
                if threeSum > 0:
                    right -= 1
                elif threeSum < 0:
                    left += 1
                else:
                    result.append([nums[i], nums[right], nums[left]])
                    left += 1
                    while nums[left] == nums[left-1] and left < right:
                        left += 1

        return result

obj = Solution()
nums = [-1,0,1,2,-1,-4]
print(obj.threeSum(nums))
