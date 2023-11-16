class Solution:
    def maxArea(self, height: list[int]) -> int:
        result = 0
        n = len(height)
        left , right = 0, n-1
        while left < right:
            current_area = min(height[left], height[right]) * (right - left)
            result = max(result, current_area)
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return result


obj = Solution()
nums = [1, 2, 150, 2, 5, 4, 8, 130, 2]
print(obj.maxArea(nums))
