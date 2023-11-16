import pygame
import random
from config import UNIT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR
from src.wall import Wall
from src.gold import Gold
from src.player import Player

pygame.init()
bg = pygame.Color(BACKGROUND_COLOR)
screen = pygame.display.set_mode((SCREEN_WIDTH * UNIT_SIZE, SCREEN_HEIGHT * UNIT_SIZE))
screen.fill(bg)

wallImage = pygame.image.load("assets/wall5.png").convert()
playerImage = pygame.image.load("assets/player.png").convert()
coinImage = pygame.image.load("assets/coin1.png").convert()

class Maze():
    def __init__(self):
        self.walls = []
        self.gold = []
        self.startPointH = 0
        self.startPointW = 0
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.generate()

    # Randomized Prim’s Algorithm
    def generate(self):
        ##########
        # private functions
        def create_empty_grid(grid = []):
            for i in range(0, self.height):
                line = []
                for j in range(0, self.width):
                    line.append('u')
                grid.append(line)
            return grid
        
        def set_borders(grid):
            for i in range(0,self.width):
                grid[0][i] = 'w'
                grid[self.height-1][i] = 'w'
            for i in range(0,self.height):
                grid[i][0] = 'w'
                grid[i][self.width-1] = 'w'
        
        def set_start_point(grid):
            self.startPointH = random.randint(1,self.height-1)
            self.startPointW = random.randint(1,self.width-1)
            grid[self.startPointH][self.startPointW] = 'c'

        def mark_starting_point_surroundings_as_walls(grid, wallList):
            if self.startPointH-1 > 0:
                wallList.append([self.startPointH-1, self.startPointW])
                grid[self.startPointH-1][self.startPointW] = 'w'
            if self.startPointW-1 > 0:
                wallList.append([self.startPointH, self.startPointW-1])
                grid[self.startPointH][self.startPointW-1] = 'w'
            if self.startPointW+1 < self.width:
                wallList.append([self.startPointH, self.startPointW+1])
                grid[self.startPointH][self.startPointW+1] = 'w'
            if self.startPointH+1 < self.height:
                wallList.append([self.startPointH+1, self.startPointW])
                grid[self.startPointH+1][self.startPointW] = 'w'
        
        def surrounding_cells_count(grid, rand_wall):
            s_cells = 0
            rand_wall_h = rand_wall[0]
            rand_wall_w = rand_wall[1]
            if (grid[rand_wall_h-1][rand_wall_w] == 'c'):
                s_cells += 1
            if (grid[rand_wall_h+1][rand_wall_w] == 'c'):
                s_cells += 1
            if (grid[rand_wall_h][rand_wall_w-1] == 'c'):
                s_cells +=1
            if (grid[rand_wall_h][rand_wall_w+1] == 'c'):
                s_cells += 1
            return s_cells
        
        def select_cell_or_gold():
            population = ['c', 'g']
            weights = [0.95, 0.05]
            chosen = random.choices(population, weights)
            return chosen[0]

        def check_and_mark_cell_or_gold(grid, rand_wall):
            s_cells = surrounding_cells_count(grid, rand_wall)
            if s_cells < 2:
                grid[rand_wall[0]][rand_wall[1]] = select_cell_or_gold()  


        def delete_wall(wallList, rand_wall):
            for wall in wallList:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    wallList.remove(wall)

        def update_grid_and_wallList(grid, wallList, rand_wall):
            rand_wall_h = rand_wall[0]
            rand_wall_w = rand_wall[1]
            if rand_wall_h != 0:
                if grid[rand_wall_h-1][rand_wall_w] != 'c':
                    grid[rand_wall_h-1][rand_wall_w] = 'w'
                    if [rand_wall_h-1, rand_wall_w] not in wallList:
                        wallList.append([rand_wall_h-1, rand_wall_w])
            if rand_wall_h != self.height-1:
                if grid[rand_wall_h+1][rand_wall_w] != 'c':
                    grid[rand_wall_h+1][rand_wall_w] = 'w'
                    if [rand_wall_h+1, rand_wall_w] not in wallList:
                        wallList.append([rand_wall_h+1, rand_wall_w])
            if rand_wall_w != 0:
                if grid[rand_wall_h][rand_wall_w-1] != 'c':
                    grid[rand_wall_h][rand_wall_w-1] = 'w'
                    if [rand_wall_h, rand_wall_w-1] not in wallList:
                        wallList.append([rand_wall_h, rand_wall_w-1])
            if rand_wall_w != self.width-1:
                if grid[rand_wall_h][rand_wall_w+1] != 'c':
                    grid[rand_wall_h][rand_wall_w+1] = 'w'
                    if [rand_wall_h, rand_wall_w+1] not in wallList:
                        wallList.append([rand_wall_h, rand_wall_w+1])
        
        def update_checked_wall(grid, wallList, rand_wall):
            check_and_mark_cell_or_gold(grid, rand_wall)
            update_grid_and_wallList(grid, wallList, rand_wall)
            delete_wall(wallList, rand_wall)

        def mark_unvisited_cells_as_wall(grid):
            for i in range(0, len(grid)):
                for j in range(0, len(grid[0])):
                    if grid[i][j] == 'u':
                        grid[i][j] = 'w'

        def drawMaze(grid):
            for h in range(0,self.height):
                for w in range(0,self.width):
                    if grid[h][w] == 'w':
                        self.walls.append(Wall(w * UNIT_SIZE, h * UNIT_SIZE, wallImage, screen))
                    if grid[h][w] == 'g':
                        self.gold.append(Gold(w * UNIT_SIZE, h * UNIT_SIZE, coinImage, screen))
        ##########

        # wallList stores coordinates of walls to be checked
        # cells next to the starting point are marked as walls
        wallList = []
        grid = create_empty_grid()
        # set_borders(grid)
        set_start_point(grid)
        mark_starting_point_surroundings_as_walls(grid, wallList)
        
        # while there are walls to be checked
        # choose a random wall from the list
        # check if it is a wall between cell and unvisited cell
        # if it is, change it to cell and mark the unvisited cell as wall
        while wallList:
            rand_wall = wallList[random.randint(1,len(wallList))-1]
            rand_wall_h = rand_wall[0]
            rand_wall_w = rand_wall[1]
            if rand_wall_w != 0:
                if grid[rand_wall_h][rand_wall_w-1] == 'u' and grid[rand_wall_h][rand_wall_w+1] == 'c':
                    update_checked_wall(grid, wallList, rand_wall)
                    continue
               
            if rand_wall_h != 0:  
                if grid[rand_wall_h-1][rand_wall_w] == 'u' and grid[rand_wall_h+1][rand_wall_w] == 'c':
                    update_checked_wall(grid, wallList, rand_wall)
                    continue
              
            if rand_wall_h != self.height-1:
                if grid[rand_wall_h+1][rand_wall_w] == 'u' and grid[rand_wall_h-1][rand_wall_w] == 'c':
                    update_checked_wall(grid, wallList, rand_wall)
                    continue
               
            if rand_wall_w != self.width-1:
                if grid[rand_wall_h][rand_wall_w+1] == 'u' and grid[rand_wall_h][rand_wall_w-1] == 'c':
                    update_checked_wall(grid, wallList, rand_wall)
                    continue
                
            delete_wall(wallList, rand_wall)
        set_borders(grid)
        mark_unvisited_cells_as_wall(grid)
        drawMaze(grid)


maze = Maze()
player = Player(maze.startPointW * UNIT_SIZE, maze.startPointH * UNIT_SIZE, playerImage, screen)
playerMove = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_LEFT:
                playerMove = 'left'
            if key == pygame.K_RIGHT:
                playerMove = 'right'
            if key == pygame.K_UP:
                playerMove = 'up'
            if key == pygame.K_DOWN:
                playerMove = 'down'
        if event.type == pygame.KEYUP:
           playerMove = False

    screen.fill(bg)
    for gold in maze.gold:
        gold.draw()
        if player.area.colliderect(gold.area):
            maze.gold.remove(gold)

    player_wall_collisions = []
    player_wall_collision_left = player.area.copy().move(-1, 0)
    player_wall_collision_right = player.area.copy().move(1, 0)
    player_wall_collision_up = player.area.copy().move(0, -1)
    player_wall_collision_down = player.area.copy().move(0, 1)
    for wall in maze.walls:
        wall.draw()
        if player_wall_collision_left.colliderect(wall.area):
            player_wall_collisions.append('left')
        if player_wall_collision_right.colliderect(wall.area):
            player_wall_collisions.append('right')
        if player_wall_collision_up.colliderect(wall.area):
            player_wall_collisions.append('up')
        if player_wall_collision_down.colliderect(wall.area):
            player_wall_collisions.append('down')


    if not playerMove in player_wall_collisions:  
        player.makeMove(playerMove)

    player.draw()

    pygame.time.wait(30)
    pygame.display.update()