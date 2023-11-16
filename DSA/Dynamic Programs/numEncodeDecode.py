class Solution:
    def numDecodings(self, s: str) -> int:
        result = 0
        # encode_dict = {}
        # for i in range(26):
        #     encode_dict[chr(ord('a')+i)] = i+1
        # print(encode_dict)
        n = len(s)
        dp = [0] * n
        for i in range(n+1):
            print(s[i])
            for j in range(n-1):
                print(s[j], s[j-1])
        return result

obj = Solution()
s = "226548"
print(obj.numDecodings(s))