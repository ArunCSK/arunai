class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        # Initialize an array to store the minimum number of coins for each amount
        dp = [float('inf')] * (amount + 1)
        # The minimum number of coins needed to make up amount 0 is 0
        dp[0] = 0

        # Fill the dp array for each amount from 1 to amount
        for i in range(1, amount + 1):
            for coin in coins:
                if i - coin >= 0:
                    dp[i] = min(dp[i], dp[i - coin] + 1)

        # If dp[amount] is still infinite, no combination of coins can make up the amount
        return dp[amount] if dp[amount] != float('inf') else -1

obj = Solution()
coins = [1,2,5]
amount = 11
print(obj.coinChange(coins, amount))