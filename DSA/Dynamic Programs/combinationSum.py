class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        # result = []
        # n = len(candidates)
        # result = [0] * (target + 1)
        # dict_comb_sum = {}
        # dict_comb_sum[0] = [0]
        # for i in range(1, target+1):
        #     for j in range(n):
        #         left, right = j+1, n-1
        #         while left < right:
        #             result[i] = candidates[j] + candidates[left] + candidates[right]
        #             if result[i] < target:
        #                 left += 1
        #             else:
        #                 right -= 1
        #             # dict_comb_sum[i].extend([candidates[j] + candidates[left] + candidates[right]])
        # print(dict_comb_sum)
        # return result
        def backtrack(start, target, path):
            if target == 0:
                result.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > target:
                    continue
                path.append(candidates[i])
                # Use the same candidate again, so the start index remains the same
                backtrack(i, target - candidates[i], path)
                path.pop()

        result = []
        candidates.sort()  # Sort the candidates to handle duplicates
        backtrack(0, target, [])
        return result


obj = Solution()
candidates = [2,3,5,7,9]
target = 11
print(obj.combinationSum(candidates,target))