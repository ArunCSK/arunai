class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        self.grouped_dict,self.group_distinct,self.group_distinct_sort = {}, [],[]
        self.group_distinct =[items for items in strs if items not in self.group_distinct]
        for g in range(len(self.group_distinct)):
            self.group_distinct[g] = ''.join(sorted(self.group_distinct[g]))
            if self.group_distinct[g] not in self.group_distinct_sort:
                self.group_distinct_sort.append(self.group_distinct[g])
                self.grouped_dict[self.group_distinct[g]] = []
        print(self.grouped_dict)

        for s in strs:
            temp_sort_element = ''.join(sorted(s))
            if temp_sort_element not in self.grouped_dict:
                self.grouped_dict[temp_sort_element].append(s)
            else:
                self.grouped_dict[temp_sort_element].append(s)

        return list(self.grouped_dict.values())



obj=Solution()
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(obj.groupAnagrams(strs))
