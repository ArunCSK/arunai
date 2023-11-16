class Solution:
    def rob(self, nums: list[int]) -> int:
        # result = 0
        # n = len(nums)
        # adj_flag = True
        # non_adj1 , non_adj2 = [],[]
        # for i in range(n):
        #     if adj_flag:
        #         non_adj1.append(nums[i])
        #         adj_flag = False
        #     else:
        #         non_adj2.append(nums[i])
        #         adj_flag = True
        #
        # # print(non_adj1, non_adj2)
        # # print(max(sum(non_adj1), sum(non_adj2)))
        # result = max(sum(non_adj1), sum(non_adj2))
        # return result
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return nums[0]

        # Initialize an array to store the maximum amount of money that can be robbed up to each house
        dp = [0] * n

        # The base cases
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])

        # Fill the dp array for each house
        for i in range(2, n):
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
        print(dp)
        # The result is the maximum amount of money that can be robbed from the last house
        return dp[-1]

obj = Solution()
nums = [2,1,1,2]
print(obj.rob(nums))
