class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        result = 0
        dp = [[0]*n]*m
        dest_path = (m-1, n-1)
        for row in dp:
            print(row)
        print(dp[2][6])
        return result

obj = Solution()
m = 3
n = 7
print(obj.uniquePaths(m,n))