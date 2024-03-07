import numpy as np
import sys
from map import Map
import time
import threading



class Node:
    def __init__(self,position=None,parent=None):
        self.position = position
        self.parent = parent
        self.dist = float("inf")
    def set_node_dist(self,dist):
        self.dist = dist

    def __eq__(self, other):
        return self.position == other.position

class Dijkstra:
    def __init__(self,map):
        self.map = map
        self.adjacent_squares = [(0,1),(0,-1),(1,0),(-1,0)]


    def run_step(self):
        self.map.set_gridmap(self.x,self.x,4)
        time.sleep(1)
        self.x +=1

    def draw_path(self,last_point):
        path = []
        curr_path_node = last_point
        while curr_path_node is not None:
            path.append(curr_path_node)
            curr_path_node = curr_path_node.parent
        for step in path:
            if self.map.get_square_status(step.position[0],step.position[1]) in (2,3):
                continue
            self.map.set_gridmap(step.position[0],step.position[1],6)


    def add_proper_neighbours_to_children_list(self,current_node,children):

        for new_position in self.adjacent_squares:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            #check in map or not
            if node_position[0] < 0 or node_position[1] < 0 or \
                node_position[0] > self.map.N_ROW-1 or  node_position[1] > self.map.N_COLUMN-1:
                continue

            if self.map.get_square_status(node_position[0],node_position[1]) == 1:
                continue

            
            new_node = Node(node_position,current_node)
            children.append(new_node)


    def add_proper_children_to_open_list(self,current_node,children):
                
        for child in children:
            
            if child in self.closedlist:
                continue

            if child not in self.openlist or child.dist > child.parent.dist + 10:
                child.set_node_dist(child.parent.dist + 10)
                child.parent = current_node
                if child not in self.openlist:
                    self.openlist.append(child)
                    if child != self.finishing_node:
                        self.map.set_gridmap(child.position[0],child.position[1],4)

    def is_search_finished(self,current_node):
        if current_node == self.finishing_node:
            self.draw_path(current_node)
            return 1

    def find_shortest_dist_open_node(self,optimal_node,optimal_node_idx):
        for idx,node in enumerate(self.openlist):
            if optimal_node.dist > node.dist:
                optimal_node = node
                optimal_node_idx = idx
        return optimal_node, optimal_node_idx


    def run(self):
        overtime_counter = 0
        self.closedlist = []

        start_pos = self.map.get_start_position()
        finish_pos = self.map.get_finish_position()
        self.starting_node = Node(start_pos)
        self.finishing_node = Node(finish_pos)

        

        self.starting_node.set_node_dist(0)
        
        
        self.openlist = []
        self.openlist.append(self.starting_node)
        
        
        while True:
            if len(self.openlist) == 0:
                return
            if overtime_counter > 1e5:
                return
            
            current_node = self.openlist[0]
            current_index = 0


            current_node,current_index = self.find_shortest_dist_open_node(current_node,current_index)


            self.openlist.pop(current_index)
            self.closedlist.append(current_node)

            if current_node != self.starting_node and current_node != self.finishing_node:
                    self.map.set_gridmap(current_node.position[0],current_node.position[1],5)
                
            if (self.is_search_finished(current_node)):
                return

            children = []
            self.add_proper_neighbours_to_children_list(current_node,children)
            self.add_proper_children_to_open_list(current_node,children)


            time.sleep(0.002)
            overtime_counter += 1

        



        

    
