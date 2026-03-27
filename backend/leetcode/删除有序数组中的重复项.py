class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0
        
        # slow 指针表示当前存放唯一元素的索引
        slow = 0
        
        # fast 指针遍历整个数组
        for fast in range(1, len(nums)):
            # 如果发现一个新元素（与当前 slow 指向的元素不同）
            if nums[fast] != nums[slow]:
                slow += 1
                # 将这个新元素搬到 slow 的下一个位置
                nums[slow] = nums[fast]
        
        # 返回唯一元素的个数，即索引 + 1
        return slow + 1
    

nums = [1,1,2]
test = Solution()
print(test.removeDuplicates(nums))