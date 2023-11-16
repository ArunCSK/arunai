class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        # result = False
        # splited_words = {}
        # for c, items in enumerate(wordDict):
        #     if items in s:
        #         splited_words[items] = c
        # # print(splited_words)
        # str_space = ''
        # for sw in splited_words:
        #     for i in s.split(sw):
        #         if i == sw:
        #             i = i + ' '
        #             str_space += i
        #     print(str_space)
        # return result
        n = len(s)
        dp = [False] * (n+1)
        wordSet = set(wordDict)
        dp[0] = True

        for i in range(1, n+1):
            for j in range(i):
                if dp[j] and s[j:i] in wordSet:
                    dp[i] = True
                    break
        print(dp)
        return dp[n]

obj =Solution()
s = "applepenapple"
wordDict = ["apple","pen"]
print(obj.wordBreak(s, wordDict))