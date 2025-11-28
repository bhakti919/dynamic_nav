# astar.py
import heapq
import numpy as np

class AStar:
    def __init__(self, grid):
        self.grid = grid  # 0 = free, 1 = blocked

        self.rows = grid.shape[0]
        self.cols = grid.shape[1]

        self.moves = [
            (-1, 0), (1, 0), (0, -1), (0, 1)  # up, down, left, right
        ]

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_free(self, r, c):
        return self.grid[r, c] == 0

    def heuristic(self, r, c, goal):
        return abs(goal[0] - r) + abs(goal[1] - c)

    def search(self, start, goal):
        sr, sc = start
        gr, gc = goal

        pq = []
        heapq.heappush(pq, (0, (sr, sc)))

        came_from = {}
        cost = { (sr, sc): 0 }

        while pq:
            _, (r, c) = heapq.heappop(pq)

            if (r, c) == (gr, gc):
                return self.reconstruct(came_from, start, goal)

            for dr, dc in self.moves:
                nr, nc = r + dr, c + dc

                if not self.in_bounds(nr, nc): 
                    continue
                if not self.is_free(nr, nc):  
                    continue

                new_cost = cost[(r, c)] + 1

                if (nr, nc) not in cost or new_cost < cost[(nr, nc)]:
                    cost[(nr, nc)] = new_cost
                    priority = new_cost + self.heuristic(nr, nc, goal)
                    heapq.heappush(pq, (priority, (nr, nc)))
                    came_from[(nr, nc)] = (r, c)

        return None  # no path

    def reconstruct(self, came_from, start, goal):
        path = []
        node = goal
        while node != start:
            path.append(node)
            node = came_from[node]
        path.append(start)
        return path[::-1]
