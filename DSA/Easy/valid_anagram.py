class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) == len(t):
            stringElements = self.checkStringElements(s, t)
            if sorted(s) == sorted(t) and stringElements:
                return True
        return False

    def checkStringElements(self, src_string, trg_string) -> bool:
        temp_src_string, temp_trg_string = src_string, trg_string
        for s in src_string:
            for t in trg_string:
                if s in trg_string and t in src_string:
                    continue
                else:
                    return False
        return True


obj = Solution()
s = "anagramr"
t = "nagaramt"
print(obj.isAnagram(s, t))