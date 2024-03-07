import pygame
import numpy as np
import sys

"TO BE ADDED: THE DENSITY OF THE OBSTACLES SHOULD BE CHANGED AND MOUSE INPUT SHOULD BE ADDED FOR OBSTACLES"
class Map:
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)
    RED = (200, 0, 0)
    GREEN = (0, 200, 0)
    BLUE = (0, 0, 200)
    PURPLE = (128, 0, 128)
    GRAY = (128, 128, 128)

    grid_based = 1


    GRID_WINDOW_HEIGHT = 900
    GRID_WINDOW_WIDTH = 900

    WINDOW_HEIGHT = 900
    WINDOW_WIDTH = 1200
    BLOCK_SIZE = 30

    N_ROW = int(GRID_WINDOW_WIDTH / BLOCK_SIZE)
    N_COLUMN = int(GRID_WINDOW_HEIGHT / BLOCK_SIZE)

    def __init__(self):
        pygame.init()
        self.SCREEN = pygame.display.set_mode((Map.WINDOW_WIDTH, Map.WINDOW_HEIGHT))
        self.CLOCK = pygame.time.Clock()
        self.SCREEN.fill(Map.WHITE)
        self.button_list = []
        self.lock_buttons = False
        self.edges = []
        self.grid_map = np.zeros((Map.N_ROW,Map.N_COLUMN))
        self.number_of_obstacles = 250
        self.obstacle_list = []
        self.lowest_start_finish_distance = 18
        self.user_menu_setup()

        self.random_start_finish_generator(self.lowest_start_finish_distance)

    def set_gridmap(self,x,y,value):
        self.grid_map[x,y] = value
    
    def reset_gridmap(self,erase_obstacles = 0,erase_algorithm_results = 0,erase_start_finish = 0):
        if erase_obstacles:
            mask = np.isin(self.grid_map, [1])
            self.grid_map[mask] = 0
        if erase_algorithm_results:
            self.edges = []
            mask = np.isin(self.grid_map, [4,5,6])
            self.grid_map[mask] = 0
        if erase_start_finish:
            mask = np.isin(self.grid_map, [2,3])
            self.grid_map[mask] = 0

    def get_start_position(self,grid_based = 1):
        i,j = np.where(self.grid_map == 3)
        if not grid_based:
            i[0] = i[0] * Map.BLOCK_SIZE +  Map.BLOCK_SIZE/2
            j[0] = j[0] * Map.BLOCK_SIZE +  Map.BLOCK_SIZE/2
        return i[0],j[0]

    def get_finish_position(self,grid_based = 1):
        i,j =  np.where(self.grid_map == 2)
        if not grid_based:
            i[0] = i[0] * Map.BLOCK_SIZE +  Map.BLOCK_SIZE/2
            j[0] = j[0] * Map.BLOCK_SIZE +  Map.BLOCK_SIZE/2 
        return i[0],j[0]


    def get_square_status(self,x,y):
        return self.grid_map[x,y]
    
    def random_obstacle_generator(self,count):
        self.reset_gridmap(erase_algorithm_results = 1,erase_obstacles = 1)
        obstacle_x_index = np.random.randint(0,Map.N_ROW,count)
        obstacle_y_index = np.random.randint(0,Map.N_COLUMN,count)
        self.set_gridmap(obstacle_x_index,obstacle_y_index, 1)
        self.obstacle_list = list(zip(obstacle_x_index*Map.BLOCK_SIZE,obstacle_y_index*Map.BLOCK_SIZE))
        self.set_start_finish()

    def random_start_finish_generator(self,req_distance,button_pressed=0):
        if button_pressed:
            self.reset_gridmap(erase_algorithm_results=1,erase_start_finish=1)
            self.reset_start_finish()
        max_max_dist = 0
        self.x_idxs = [0,0]
        self.y_idxs = [0,0]
        
        for i in range(100):
            start_finish_x_indexs = np.random.randint(0,Map.N_ROW,2)
            start_finish_y_indexs = np.random.randint(0,Map.N_COLUMN,2)
            manhattan_dist = [abs(start_finish_x_indexs[0]- start_finish_x_indexs[1]) , abs(start_finish_y_indexs[0]- start_finish_y_indexs[1])]
            curr_max_dist = max(manhattan_dist)
            if curr_max_dist > max_max_dist:
                self.x_idxs = start_finish_x_indexs
                self.y_idxs = start_finish_y_indexs
                max_max_dist = curr_max_dist
            if curr_max_dist > req_distance:
                break
        self.set_start_finish()
    
    def draw_line(screen,lines):
        for line,color in lines:
            pygame.draw.line(screen,color , line[0], line[1],3)

    def draw_square(screen,x,y,size,square_status,grid_based):
        width = 0
        if square_status == 0:
            color = Map.WHITE
        elif square_status == 1:
            color = Map.BLACK
        elif square_status == 2:
            color = Map.RED
        elif square_status == 3:
            color = Map.GREEN
        elif square_status == 4:
            color = Map.BLUE
        elif square_status == 5:
            color = Map.PURPLE
        elif square_status == 6:
            color = Map.GRAY
        

        rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(screen, color, rect, width)
        
        if grid_based == 1:
            rect = pygame.Rect(x, y, size, size)
            pygame.draw.rect(screen, Map.BLACK, rect, 1)






    def button_function_handler(self,func, *args, **kwargs):
        def wrapper():
            return func(*args, **kwargs)
        return wrapper

    def button(self,text,font_size,x_percent,y_percent,function):
        font = pygame.font.SysFont("Arial", font_size )
        text1=font.render(text, True, Map.BLACK)
        button_center_x = Map.GRID_WINDOW_WIDTH + (Map.WINDOW_WIDTH - Map.GRID_WINDOW_WIDTH)* x_percent
        button_center_y = int(Map.WINDOW_HEIGHT * y_percent)
        button = text1.get_rect(topleft=(button_center_x,button_center_y))

        self.SCREEN.blit(text1, button)
        pygame.draw.rect(self.SCREEN, Map.BLACK,button,2)
        self.button_list.append([button,function])

    def algorithm_situation_indicator(self,button_pos, status):
        color = Map.WHITE
        if status == 1:
            color =  Map.RED
        elif status == 0:
            color = Map.GREEN

        button_center_x = Map.GRID_WINDOW_WIDTH + (Map.WINDOW_WIDTH - Map.GRID_WINDOW_WIDTH)* (button_pos[0] + 0.5)
        button_center_y = int(Map.WINDOW_HEIGHT * button_pos[1])

        rect = pygame.Rect(button_center_x, button_center_y, 70, 20)
        pygame.draw.rect(self.SCREEN, color, rect, 0)



    def user_menu_setup(self):
        pygame.draw.line(self.SCREEN, Map.BLACK, (Map.GRID_WINDOW_WIDTH,0), (Map.GRID_WINDOW_WIDTH,Map.GRID_WINDOW_HEIGHT),2)
        font_size = 24
        font = pygame.font.SysFont('Arial', font_size)
        title_center_x = Map.GRID_WINDOW_WIDTH + (Map.WINDOW_WIDTH - Map.GRID_WINDOW_WIDTH)* 0.05
        title_center_y = int(Map.WINDOW_HEIGHT * 0.05) 
        text = ["Path Finding Algorithm",
                "Testing Environment",
                "Beta version"]    
        label = []
        for line in text: 
            label.append(font.render(line, True, Map.BLACK))
        for line in range(len(label)):
            self.SCREEN.blit(label[line],(title_center_x,title_center_y+(line*font_size)+(15*line)))
        
        random_obstacles_button_handler = self.button_function_handler(self.random_obstacle_generator,self.number_of_obstacles)
        start_finish_button_handler = self.button_function_handler(self.random_start_finish_generator,self.lowest_start_finish_distance,button_pressed=1)
        
        self.set_random_obstacles_button = self.button(" Set Random Obstacles ",22,0.05,0.35,random_obstacles_button_handler)
        
        self.set_start_finish_button = self.button(" Set Different Start/Finish ",22,0.05,0.39,start_finish_button_handler)


    def reset_start_finish(self):
        self.set_gridmap(self.x_idxs,self.y_idxs, [0,0])

    def set_start_finish(self):
        self.set_gridmap(self.x_idxs,self.y_idxs, [2,3])


    def draw_map(self,grid_based):
        if grid_based:            
            for x_idx,x in enumerate(range(0, Map.GRID_WINDOW_WIDTH, Map.BLOCK_SIZE)):
                for y_idx,y in enumerate(range(0, Map.GRID_WINDOW_HEIGHT, Map.BLOCK_SIZE)):
                    square_status = self.get_square_status(x_idx,y_idx)
                    Map.draw_square(self.SCREEN,x,y,Map.BLOCK_SIZE,square_status,grid_based)
        else:
            if self.edges == []:
                for x_idx,x in enumerate(range(0, Map.GRID_WINDOW_WIDTH, Map.BLOCK_SIZE)):
                    for y_idx,y in enumerate(range(0, Map.GRID_WINDOW_HEIGHT, Map.BLOCK_SIZE)):
                        square_status = self.get_square_status(x_idx,y_idx)
                        Map.draw_square(self.SCREEN,x,y,Map.BLOCK_SIZE,square_status,grid_based)
            Map.draw_line(self.SCREEN,self.edges)                    


    def render(self,grid_based):
        self.draw_map(grid_based)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and not self.lock_buttons:
                for button,function in self.button_list:
                    if button.collidepoint(event.pos):
                        function()
                        

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        
