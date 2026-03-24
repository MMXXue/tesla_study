class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        m = 0
        result = []
        print(len(nums))

        for m in range(len(nums) - 1):
            print(f"m: {m}")
            for n in range(m+1, len(nums)):
                print(f"n: {n}")
                if nums[m] + nums[n] == target:
                    result.append(m)
                    result.append(n)
                    return result
            print(f"\n")




nums = [3,2,4]
target = 6
test = Solution()
print(test.twoSum(nums, target))