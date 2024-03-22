import numpy as np
import sys
from map import Map
import time




# bence random pointler alan disinda da atilmali ama candidate pointler alan icinde kalsin diye bir check yapilmali
# kenarlarda kalan bitis noktalarina ulasmakta zorlaniyor algoritma 

# Cok kotu STEP
# Cok kotu OBSTACLE BETWEEN   KISMINA BIR COZUM LAZIM



class Node:
    def __init__(self,position=None,parent=None):
        self.position = position
        self.parent = parent

    def __eq__(self, other):
        return self.position == other.position

class RRT:
    def __init__(self,map):
        self.map = map
        self.map_dimensions = (map.GRID_WINDOW_WIDTH,map.GRID_WINDOW_HEIGHT)

    def random_point_generator(self):
        x = np.random.randint(0,self.map_dimensions[0],1)
        y = np.random.randint(0,self.map_dimensions[1],1)
        return (x[0],y[0])

    def check_nearest_node_to_the_random_point(self,random_point):
        nearest_node = self.tree[0]
        nearest_distance = self.get_distance(self.tree[0],random_point)
        for node in self.tree:
            if nearest_distance > self.get_distance(node,random_point):
                nearest_node = node
                nearest_distance = self.get_distance(node,random_point)

        return (nearest_node,nearest_distance)

    def set_candidate_according_to_step_size(self,parent_node,random_point,step_size):
        if self.get_distance(parent_node,random_point) < self.step_size:
            return (random_point[0],random_point[1])
        if parent_node.position == random_point:
            return None
        x1, y1 = parent_node.position
        x2, y2 = random_point

        # Calculate the total distance between the two points
        total_distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        # Calculate the fraction of the total distance for the desired distance
        fraction = step_size / total_distance

        # Calculate the coordinates of the point at the desired distance
        candidate_x = x1 + fraction * (x2 - x1)
        candidate_y = y1 + fraction * (y2 - y1)
        return (candidate_x,candidate_y)

    def check_candidate_collision_with_obstacle(self,obstacle_list,obstacle_size,candidate):
        for obstacle in obstacle_list:
            x_min = obstacle[0]
            x_max = x_min + obstacle_size
            
            y_min = obstacle[1]
            y_max = y_min + obstacle_size

            if x_min <= candidate[0] <= x_max and y_min <= candidate[1] <= y_max:
                return None
        return candidate

    def check_obstacles_between_node_and_candidate(self,obstacle_list,obstacle_size,parent_node,random_point,number_of_points_in_interpolation):
        if parent_node.position == random_point:
            print("yok ebenin ami")
            return None
        x1, y1 = parent_node.position
        x2, y2 = random_point

        total_distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        
        for dist in range(0,number_of_points_in_interpolation):
            fraction = dist / total_distance
            interpolate_point_x = x1 + fraction * (x2 - x1)
            interpolate_point_y = y1 + fraction * (y2 - y1)
            no_collusion_point = self.check_candidate_collision_with_obstacle(obstacle_list,obstacle_size,(interpolate_point_x,interpolate_point_y))
        
            if no_collusion_point is None:
                return None
    

        return 1

    def add_the_candidate_to_tree(self,candidate_point,parent_node,obstacle_passing_feasibility):
        
        if candidate_point is not None and obstacle_passing_feasibility is not None:
            candidate_node = Node(candidate_point,parent_node)
            self.tree.append(candidate_node)
            return candidate_node
        return None


    def draw_path(self,last_node):
        path = []
        curr_node = last_node
        while curr_node.parent is not None:
            path.append(curr_node)
            curr_node = curr_node.parent
        for step in path:
            self.map.edges[self.map.edges.index([[step.parent.position,step.position],(200,0,0)])] = [[step.parent.position,step.position],(0,0,200)]



    def get_distance(self,node,random_point):
        x_dist = (node.position[0] - random_point[0]) ** 2
        y_dist = (node.position[1] - random_point[1]) ** 2
        return np.sqrt(x_dist + y_dist)


    def is_search_finished(self,current_point,epsilon):
        dist_to_finish = self.get_distance(self.finishing_node,current_point)

        if dist_to_finish < epsilon:
            return 1
        return 0


    def run(self):
        epsilon = 30
        self.step_size = 20

        number_of_iterations = 1e3
        self.tree = []
        finished = 0
        start_pos = self.map.get_start_position(grid_based = 0)
        finish_pos = self.map.get_finish_position(grid_based = 0)
        self.starting_node = Node(start_pos)
        self.finishing_node = Node(finish_pos)
        self.tree.append(self.starting_node)

        for i in range(0,number_of_iterations):

            random_point = self.random_point_generator()
            parent_node,_ = self.check_nearest_node_to_the_random_point(random_point)
            candidate_point = self.set_candidate_according_to_step_size(parent_node,random_point,self.step_size)
            if candidate_point is None:
                continue
            candidate_point = self.check_candidate_collision_with_obstacle(self.map.obstacle_list,self.map.BLOCK_SIZE,candidate_point)
            obstacle_passing_feasibility = self.check_obstacles_between_node_and_candidate(self.map.obstacle_list,self.map.BLOCK_SIZE,parent_node,random_point,50)
            

            candidate_node = self.add_the_candidate_to_tree(candidate_point,parent_node,obstacle_passing_feasibility)

            if candidate_node is None:
                continue

            if candidate_node.parent is not None:
                self.map.edges.append([[candidate_node.parent.position,candidate_node.position],(200,0,0)])
            finished = self.is_search_finished(candidate_point,epsilon)


            if finished == 1:
                self.draw_path(candidate_node)
                break



            time.sleep(0.002)



        

    
