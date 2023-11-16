class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        while n:
            count += n & 1
            n >> 1
        return count


obj = Solution()
n = int("00000000000000000000000000001011", 2)
print(obj.hammingWeight(n))