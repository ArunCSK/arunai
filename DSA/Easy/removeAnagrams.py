from collections import Counter

class Solution:
    def removeAnagrams(self, words: list[str]) -> list[str]:

        distict_list, anagrams_count= [], {}

        for w in words:
            w = ''.join(sorted(w))
            if w not in distict_list:
                distict_list.append(w)

        result = []
        counter = Counter(words)
        for i, f in counter.items():
            print(i, f)

        result = []
        for i in range(len(words)):
            w = ''.join(sorted(words[i]))


        print(result)

        return words


obj = Solution()
words = ["abba", "baba", "bbaa", "cd", "cd"]
print(obj.removeAnagrams(words))


