from typing import List, Any

import numpy as np


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.f = 0
        self.h = 0
        self.g = 0


def astar(maze, start, end):
    startNode = Node(None, start)
    endNode = Node(None, end)

    openList = []
    closedList = []

    openList.append(startNode)

    while len(openList) > 0:
        currentNode = openList[0]
        currentIndex = 0

        for index, item in enumerate(openList):
            if item.f < currentNode.f:
                currentNode = item
                currentIndex = index
        openList.pop(currentIndex)
        closedList.append(currentNode)

        if currentNode.position == endNode.position:
            path = []
            curr = currentNode
            while curr is not None:
                path.append(curr.position)
                curr = curr.parent
            return path[::-1]

        children = []
        positions = [(0, -1), (0, 1), (1, 0), (-1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)]
        for poss in positions:
            nodePoss = (currentNode.position[0] + poss[0], currentNode.position[1] + poss[1])
            # check that child poss are all in the maze range
            if nodePoss[0] > maze.shape[0]-1 or nodePoss[0] < 0 or nodePoss[1] > maze.shape[1]-1 or nodePoss[1] < 0:
                continue
            # is it an obstacle or a path
            if maze[nodePoss[0]][nodePoss[1]] != 0:
                continue

            newNode = Node(currentNode, nodePoss)
            children.append(newNode)
        for child in children:
            for closed in closedList:
                if closed == child:
                    continue
            child.g = currentNode.g + 1
            child.h = ((child.position[0] - endNode.position[0]) ** 2) + (
                    (child.position[1] - endNode.position[1]) ** 2)
            child.f = child.g + child.h

            for opens in openList:
                if opens.position == child.position and opens.g < child.g:
                    continue

            openList.append(child)


def coordinateFinder(num):
    x = num % 36
    y = int((num - x) / 36)
    return x, y


def main(start, end, obstacles):
    maze = np.zeros((36, 30))

    startCoordinate = coordinateFinder(start)
    endCoordinate = coordinateFinder(end)

    for obstacle in obstacles:
        obs_x,obs_y = coordinateFinder(obstacle)
        print(obs_x)
        print(obs_y)

        maze[obs_x,obs_y] = 1
    path = astar(maze, startCoordinate, endCoordinate)
    return path


