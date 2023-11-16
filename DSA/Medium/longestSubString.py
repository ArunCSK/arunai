class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_index_map = {}  # Store the index of each character's last occurrence
        start = max_length = 0
        for end, char in enumerate(s):
            if char in char_index_map and char_index_map[char] >= start:
                start = char_index_map[char] + 1

            char_index_map[char] = end
            max_length = max(max_length, end - start + 1)

        return max_length


        # visited = []
        # # print(len(s))
        #
        # if len(s) == 0:
        #     return 0
        # elif s.__contains__(" ") or len(s) == 1:
        #     return 1
        #
        # for i in range(len(s)):
        #     for j in range(i + 1, len(s)):
        #         visited.append(s[i:j])
        # temp_str = ''
        # subarry_dict = {}
        # for v in visited:
        #     if v not in temp_str:
        #         temp_str += v
        #     else:
        #         subarry_dict[temp_str] = len(temp_str)
        #         break
        #
        # # for v in visited:
        # #     if v not in temp_str:
        # #         temp_str += v
        # #     else:
        # #         break
        # # subarry_dict[temp_str] = len(temp_str)
        #
        # print(subarry_dict)
        # return max(subarry_dict.values())


obj = Solution()
s = "pwwkew"
print(obj.lengthOfLongestSubstring(s))



