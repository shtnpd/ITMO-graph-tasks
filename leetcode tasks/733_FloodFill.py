from collections import deque
from typing import List

class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        original_color = image[sr][sc]

        if original_color == color:
            return image
        
        rows, cols = len(image), len(image[0])
        queue = deque([(sr, sc)])
        image[sr][sc] = color

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while queue:
            r, c = queue.popleft()
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                if (0 <= nr < rows and 0 <= nc < cols and 
                    image[nr][nc] == original_color):
                    image[nr][nc] = color
                    queue.append((nr, nc))
        
        return image