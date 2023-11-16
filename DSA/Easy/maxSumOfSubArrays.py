class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        # sub_list = []
        # for i in range(len(nums)):
        #     for j in range(len(nums)):
        #         temp_list = nums[i:j+1]
        #         if temp_list not in sub_list:
        #             sub_list.append(temp_list)
        # # print(sub_list)
        # max_sum = 0
        # for s in sub_list:
        #     max_sum = max(max_sum, sum(s))
        #
        # return max_sum
        if not nums:
            return 0

        current_sum = max_sum = nums[0]

        for num in nums[1:]:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)

        return max_sum


obj = Solution()
nums = [-2,1,-3,4,-1,2,1,-5,4]
print(obj.maxSubArray(nums))
