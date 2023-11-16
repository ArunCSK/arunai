class Solution:
    def containsDuplicate(self, nums) -> bool:
        temp_list = []
        for n in nums:
            if n in temp_list:
                return True
            temp_list.append(n)
        return False



obj = Solution()
nums = [1,1,1,3,3,4,3,2,4,2]
print(obj.containsDuplicate(nums))