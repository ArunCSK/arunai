class Solution:
    def maxArea(self, height: list[int]) -> int:
        # result = 0
        # if len(set(height)) == 1:
        #     length, second_max_height = height[0], height[0]
        # else:
        #     max_height = max(height)
        #     second_max_height = max([x for x in height if x < max_height])
        #     volume_dict = {}
        #     for i, a in enumerate(height):
        #         if a == max_height or a == second_max_height:
        #             volume_dict[i] = a
        #     key_max = list(volume_dict[max_height])
        #     print(max(key_max))
        #     # length1 = height.index(second_max_height) - height.index(max_height)
        #     # length2 = height.index(max_height) - height.index(second_max_height)
        #     # if length1 > length2:
        #     #     length = length1
        #     # else:
        #     #     length = length2
        # return 0  # length*second_max_height
        max_water = 0
        left = 0
        right = len(height) - 1

        while left < right:
            h = min(height[left], height[right])
            w = right - left
            max_water = max(max_water, h * w)

            # Move the pointers towards each other
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_water

obj = Solution()
height = [4,3,2,1,4]
print(obj.maxArea(height))