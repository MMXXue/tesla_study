class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        # 暴力
        # m = 0
        # result = []
        # print(len(nums))

        # for m in range(len(nums) - 1):
        #     print(f"m: {m}")
        #     for n in range(m+1, len(nums)):
        #         print(f"n: {n}")
        #         if nums[m] + nums[n] == target:
        #             result.append(m)
        #             result.append(n)
        #             return result
        #     print(f"\n")


        # 指针
        prev_map = {}

        # enumerate总是会返回两个数值,第一个是索引,第二个是数值
        for i, n in enumerate(nums):
            diff = target - n
            if diff in prev_map:
                return [prev_map[n], i]
            prev_map[n] = i







nums = [3,2,4]
target = 6
test = Solution()
print(test.twoSum(nums, target))