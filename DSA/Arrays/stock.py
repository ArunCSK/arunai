class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        # result = 0
        # n = len(prices)
        # maxProfit = 0
        # for i in range(n+1):
        #     left, right = i, n-1
        #     while left < right:
        #         if prices[right] > prices[left]:
        #             result = max(maxProfit, prices[right] - prices[left])
        #             maxProfit = prices[right] - prices[left]
        #         left += 1
        #         right -= 1
        # return result
        if not prices or len(prices) == 1:
            return 0

        min_price = prices[0]
        max_profit = 0

        for price in prices[1:]:
            # Calculate the profit by selling at the current price
            max_profit = max(max_profit, price - min_price)
            # Update the minimum price encountered so far
            min_price = min(min_price, price)

        return max_profit

obj = Solution()
prices = [7,1,5,3,6,4]
print(obj.maxProfit(prices))