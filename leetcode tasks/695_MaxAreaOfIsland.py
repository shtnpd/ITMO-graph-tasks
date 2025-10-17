from typing import List
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        visited = set()
        max_area = 0
        
        def dfs(r: int, c: int) -> int:
            if (r < 0 or r >= rows or c < 0 or c >= cols or 
                (r, c) in visited or grid[r][c] == 0):
                return 0

            visited.add((r, c))
            
            area = 1
            area += dfs(r - 1, c)
            area += dfs(r + 1, c)
            area += dfs(r, c - 1)
            area += dfs(r, c + 1)
            
            return area
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1 and (r, c) not in visited:
                    current_area = dfs(r, c)
                    max_area = max(max_area, current_area)
        
        return max_area