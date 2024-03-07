import numpy as np
import sys
from map import Map
from dijkstra import Dijkstra
from astar import Astar
from rrt import RRT
import threading
import time



class Wrapper:
    def __init__(self):
        self.map = Map()
        self.grid_based = 0
        self.dijkstra = Dijkstra(self.map)
        self.astar = Astar(self.map)
        self.rrt = RRT(self.map)
        self.dijkstra_run_thread = threading.Thread(target=self.dijkstra.run)
        self.astar_run_thread = threading.Thread(target=self.astar.run)
        self.rrt_run_thread = threading.Thread(target=self.rrt.run)

        self.map_renderin_thread = threading.Thread(target=self.render_map)
        self.map_renderin_thread.start()

        dijkstra_button = self.map.button_function_handler(self.start_dijkstra_thread)
        self.map.button(" Run Dijkstra ",22,0.05,0.43,dijkstra_button)

        astar_button = self.map.button_function_handler(self.start_astar_thread)
        self.map.button(" Run Astar ",22,0.05,0.47,astar_button)

        rrt_button = self.map.button_function_handler(self.start_rrt_thread)
        self.map.button(" Run RRT ",22,0.05,0.51,rrt_button)


        self.main()

    def start_rrt_thread(self):
        self.grid_based = 0
        self.map.reset_gridmap(erase_algorithm_results=1)
        self.map.draw_map(grid_based=0)
        self.rrt_run_thread = threading.Thread(target=self.rrt.run)
        self.rrt_run_thread.start()

        return self.rrt_run_thread

               
    def start_dijkstra_thread(self):
        self.grid_based = 1
        self.map.reset_gridmap(erase_algorithm_results=1)
        self.dijkstra_run_thread = threading.Thread(target=self.dijkstra.run)
        self.dijkstra_run_thread.start()
        
        return self.dijkstra_run_thread

    def start_astar_thread(self):
        self.grid_based = 1
        self.map.reset_gridmap(erase_algorithm_results=1)
        self.astar_run_thread = threading.Thread(target=self.astar.run)
        self.astar_run_thread.start()
        
        return self.astar_run_thread



    def render_map(self):
        while True:
            self.map.render(self.grid_based)

    def main(self):
        while True:
            if self.dijkstra_run_thread.is_alive():
                self.map.algorithm_situation_indicator([0.05,0.43],1)
                self.map.lock_buttons = 1
                time.sleep(0.01)
            # Wait for the worker thread to finish without blocking the main thread
                self.dijkstra_run_thread.join()
                self.map.lock_buttons = 0

                self.map.algorithm_situation_indicator([0.05,0.43],0)
            elif self.astar_run_thread.is_alive():
                self.map.algorithm_situation_indicator([0.05,0.47],1)

                self.map.lock_buttons = 1
                time.sleep(0.01)
            # Wait for the worker thread to finish without blocking the main thread
                self.astar_run_thread.join()
                self.map.lock_buttons = 0

                self.map.algorithm_situation_indicator([0.05,0.47],0)

            elif self.rrt_run_thread.is_alive():
                self.map.algorithm_situation_indicator([0.05,0.51],1)

                self.map.lock_buttons = 1
                time.sleep(0.01)
            # Wait for the worker thread to finish without blocking the main thread
                self.rrt_run_thread.join()
                self.map.lock_buttons = 0

                self.map.algorithm_situation_indicator([0.05,0.51],0)




if __name__ == '__main__':
    game = Wrapper()






