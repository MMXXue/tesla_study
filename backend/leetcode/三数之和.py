class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        nums.sort()
        res = []
        n = len(nums)

        for i in range(n):
            if nums[i] > 0:
                break

            # 去重：如果当前的数字和上一个一样，直接跳过
            if i > 0 and nums[i] == nums[i-1]:
                continue
            
            l, r = i + 1, n - 1
            while l < r:
                total = nums[i] + nums[l] + nums[r]
                
                if total == 0:
                    res.append([nums[i], nums[l], nums[r]])
                    # 找到后，还要继续移动指针去寻找其他的组合
                    # 关键：找到后也要去重，避免重复的三元组
                    while l < r and nums[l] == nums[l+1]:
                        l += 1
                    while l < r and nums[r] == nums[r-1]:
                        r -= 1
                    l += 1
                    r -= 1
                elif total < 0:
                    l += 1
                else:
                    r -= 1
        return res