class Solution:
    def reverseBits(self, n: int) -> int:
        # result = 0
        # for _ in range(32):
        #     result = (result << 1) | (n & 1)
        #     n >>= 1
        # return result

        result = 0
        for i in range(32):
            bit = (n >> i) & 1
            result = result | (bit << (31-i))
        return result

obj = Solution()
n = int("00000010100101000001111010011100",2)
print(obj.reverseBits(n))