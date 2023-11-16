class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:

        m,n = len(text1), len(text2)
        result = [[0]*(n+1) for _ in range(m+1)]

        for i in range(1, m+1):
            for j in range(1,n+1):
                # print(text1[i-1], text2[j-1])
                if text1[i-1] == text2[j-1]:
                    result[i][j] = result[i-1][j-1]+1
                else:
                    result[i][j] = max(result[i-1][j], result[i][j-1])


        return result[m][n]

obj = Solution()
text1 = "abcde"
text2 = "ace"
print(obj.longestCommonSubsequence(text1, text2))