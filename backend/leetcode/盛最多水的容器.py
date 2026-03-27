class Solution(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        left = 0
        right = len(height) - 1
        max_water = 0

        while left < right:
            # 计算当前容量
            current_height = min(height[left], height[right])
            current_width = right - left
            current_water = current_height * current_width
            
            # 更新最大值
            max_water = max(max_water, current_water)
            
            # 移动短的那一根
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
                
        return max_water