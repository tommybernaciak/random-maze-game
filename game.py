import pygame
import random

pygame.init()
bg = pygame.Color("#8f9943")
unitSize = 16
speed = 4
screenWidth = 60
screenHeight = 40
screen = pygame.display.set_mode((screenWidth * unitSize, screenHeight * unitSize))
screen.fill(bg)
initialPlayerX = 16
initialPlayerY = 16

wallImage = pygame.image.load("wall5.png").convert()
playerImage = pygame.image.load("player.png").convert()

class Maze():
    def __init__(self):
        self.walls = []
        self.startPointH = 0
        self.startPointW = 0
        self.width = screenWidth
        self.height = screenHeight
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

        def check_and_mark_cell(grid, rand_wall):
            s_cells = surrounding_cells_count(grid, rand_wall)
            if s_cells < 2:
                grid[rand_wall[0]][rand_wall[1]] = 'c'  


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
        
        def mark_cell_and_update(grid, wallList, rand_wall):
            check_and_mark_cell(grid, rand_wall)
            update_grid_and_wallList(grid, wallList, rand_wall)
            delete_wall(wallList, rand_wall)

        def mark_unvisited_cells_as_wall(grid):
            for i in range(0, len(grid)):
                for j in range(0, len(grid[0])):
                    if grid[i][j] == 'u':
                        grid[i][j] = 'w'

        def drawWalls(grid):
            for i in range(0,self.height):
                for j in range(0,self.width):
                    if grid[i][j] == 'w':
                        self.walls.append(Wall(j * unitSize, i * unitSize, wallImage))
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
                    mark_cell_and_update(grid, wallList, rand_wall)
                    continue
               
            if rand_wall_h != 0:  
                if grid[rand_wall_h-1][rand_wall_w] == 'u' and grid[rand_wall_h+1][rand_wall_w] == 'c':
                    mark_cell_and_update(grid, wallList, rand_wall)
                    continue
              
            if rand_wall_h != self.height-1:
                if grid[rand_wall_h+1][rand_wall_w] == 'u' and grid[rand_wall_h-1][rand_wall_w] == 'c':
                    mark_cell_and_update(grid, wallList, rand_wall)
                    continue
               
            if rand_wall_w != self.width-1:
                if grid[rand_wall_h][rand_wall_w+1] == 'u' and grid[rand_wall_h][rand_wall_w-1] == 'c':
                    mark_cell_and_update(grid, wallList, rand_wall)
                    continue
                
            delete_wall(wallList, rand_wall)
        set_borders(grid)
        mark_unvisited_cells_as_wall(grid)
        ##########
        # print - debug
        # print(self.startPointW, self.startPointH)
        # for i in range(0, len(grid)):
        #     for j in range(0, len(grid[0])):
        #         print(grid[i][j], end="")
        #     print('\n')
        ##########
        drawWalls(grid)
    

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.area = pygame.Rect(self.x, self.y, unitSize, unitSize)

    def draw(self):
        screen.blit(self.image, self.area)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.area = pygame.Rect(self.x, self.y, unitSize, unitSize)
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    def move(self, x, y):
        self.x += x
        self.y += y
        self.area = pygame.Rect(self.x, self.y, unitSize, unitSize)
    def moveLeft(self):
        self.move(-speed, 0)
    def moveRight(self):
        self.move(speed, 0)
    def moveUp(self):
        self.move(0, -speed)
    def moveDown(self):
        self.move(0, speed)
    def makeMove(self, dir):
        if dir == 'left':
            self.moveLeft()
        if dir == 'right':
            self.moveRight()
        if dir == 'up':
            self.moveUp()
        if dir == 'down':
            self.moveDown()

maze = Maze()
player = Player(maze.startPointW * unitSize, maze.startPointH * unitSize, playerImage)
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
    collision = []
    playerCollisionLeft = player.area.copy().move(-1, 0)
    playerCollisionRight = player.area.copy().move(1, 0)
    playerCollisionUp = player.area.copy().move(0, -1)
    playerCollisionDown = player.area.copy().move(0, 1)
    for wall in maze.walls:
        wall.draw()
        if playerCollisionLeft.colliderect(wall.area):
            collision.append('left')
        if playerCollisionRight.colliderect(wall.area):
            collision.append('right')
        if playerCollisionUp.colliderect(wall.area):
            collision.append('up')
        if playerCollisionDown.colliderect(wall.area):
            collision.append('down')


    if not playerMove in collision:  
        player.makeMove(playerMove)

    player.draw()

    pygame.time.wait(30)
    pygame.display.update()