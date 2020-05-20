# Game of life
# Cell types version

import numpy as np
import pygame
import time

pygame.init()

width  = 700
height = 700

screen = pygame.display.set_mode((height, width))
background = 25,25,25
screen.fill(background)

cellsX = 50
cellsY = 50

dimCellWidth = width / cellsX
dimCellHeight = height / cellsY

# Cells state. Aalive = 1, dead = 0
gameState = np.zeros((cellsX, cellsY))
aliveCells = 0
redCells = 0
whiteCells = 0

# Excecution control
pauseExecution = True
endGame = False
activateOutput = False
sleepTime = 0.1

fontName = pygame.font.match_font('arial')
fontColor = (255,255,255)
bgColor = (0,0,0)
def draw_text(surface, text, size, x, y, fontColor, backgroundColor):
    font = pygame.font.Font(fontName, size)
    text_surfaceace = font.render(text, True, fontColor, backgroundColor)
    text_rect = text_surfaceace.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surfaceace, text_rect)


while not endGame:
    newGameState = np.copy(gameState)
    screen.fill(background)
    time.sleep(sleepTime)

    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            endGame = True

        if event.type == pygame.KEYDOWN:
            pauseExecution = not pauseExecution
            screen.fill(background)

        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX,posY = pygame.mouse.get_pos()
            cellX = int(np.floor(posX / dimCellWidth))
            cellY = int(np.floor(posY / dimCellHeight))
            if newGameState[cellX, cellY] == 0:
                newGameState[cellX, cellY] = 1
            elif newGameState[cellX, cellY] == 1:
                newGameState[cellX, cellY] = 2
            elif newGameState[cellX, cellY] == 2:
                newGameState[cellX, cellY] = 0

        if mouseClick[1]:
            pauseExecution = not pauseExecution



    for y in range(0, cellsX):
        for x in range (0, cellsY):
            if not pauseExecution:
                # Claculate the near neighbours
                nNeighbours = (
                      gameState[(x - 1) % cellsX, (y - 1) % cellsY]
                    + gameState[x       % cellsX, (y - 1) % cellsY]
                    + gameState[(x + 1) % cellsX, (y - 1) % cellsY]
                    + gameState[(x - 1) % cellsX,  y      % cellsY]
                    + gameState[(x + 1) % cellsX,  y      % cellsY]
                    + gameState[(x - 1) % cellsX, (y + 1) % cellsY]
                    + gameState[x      % cellsX,  (y + 1) % cellsY]
                    + gameState[(x + 1) % cellsX, (y + 1) % cellsY]
                )

                nWhiteNeighbours = (
                      ((gameState[(x - 1) % cellsX, (y - 1) % cellsY]) if (gameState[(x - 1) % cellsX, (y - 1) % cellsY]) == 1 else 0)
                    + ((gameState[x       % cellsX, (y - 1) % cellsY]) if (gameState[x       % cellsX, (y - 1) % cellsY]) == 1 else 0)
                    + ((gameState[(x + 1) % cellsX, (y - 1) % cellsY]) if (gameState[(x + 1) % cellsX, (y - 1) % cellsY]) == 1 else 0)
                    + ((gameState[(x - 1) % cellsX,  y      % cellsY]) if (gameState[(x - 1) % cellsX,  y      % cellsY]) == 1 else 0)
                    + ((gameState[(x + 1) % cellsX,  y      % cellsY]) if (gameState[(x + 1) % cellsX,  y      % cellsY]) == 1 else 0)
                    + ((gameState[(x - 1) % cellsX, (y + 1) % cellsY]) if (gameState[(x - 1) % cellsX, (y + 1) % cellsY]) == 1 else 0)
                    + ((gameState[x      % cellsX,  (y + 1) % cellsY]) if (gameState[x      % cellsX,  (y + 1) % cellsY]) == 1 else 0)
                    + ((gameState[(x + 1) % cellsX, (y + 1) % cellsY]) if (gameState[(x + 1) % cellsX, (y + 1) % cellsY]) == 1 else 0)
                )

                nRedNeighbours = int((
                      ((gameState[(x - 1) % cellsX, (y - 1) % cellsY]) if (gameState[(x - 1) % cellsX, (y - 1) % cellsY]) == 2 else 0)
                    + ((gameState[x       % cellsX, (y - 1) % cellsY]) if (gameState[x       % cellsX, (y - 1) % cellsY]) == 2 else 0)
                    + ((gameState[(x + 1) % cellsX, (y - 1) % cellsY]) if (gameState[(x + 1) % cellsX, (y - 1) % cellsY]) == 2 else 0)
                    + ((gameState[(x - 1) % cellsX,  y      % cellsY]) if (gameState[(x - 1) % cellsX,  y      % cellsY]) == 2 else 0)
                    + ((gameState[(x + 1) % cellsX,  y      % cellsY]) if (gameState[(x + 1) % cellsX,  y      % cellsY]) == 2 else 0)
                    + ((gameState[(x - 1) % cellsX, (y + 1) % cellsY]) if (gameState[(x - 1) % cellsX, (y + 1) % cellsY]) == 2 else 0)
                    + ((gameState[x      % cellsX,  (y + 1) % cellsY]) if (gameState[x      % cellsX,  (y + 1) % cellsY]) == 2 else 0)
                    + ((gameState[(x + 1) % cellsX, (y + 1) % cellsY]) if (gameState[(x + 1) % cellsX, (y + 1) % cellsY]) == 2 else 0)
                ) / 2)

                # Rule 1: A white dead cell with 3 alive white neighbours will revive.
                if gameState[x,y] == 0 and nWhiteNeighbours == 3:
                    newGameState[x,y] = 1
                # Rule 2: An alive cell with less than 2 or more than 3 alive cells near will die.
                elif gameState[x,y] == 1 and (nWhiteNeighbours < 2 or nWhiteNeighbours > 3):
                    newGameState[x,y] = 0
                elif gameState[x,y] == 0 and (nRedNeighbours == 3):
                    newGameState[x,y] = 2
                elif gameState[x,y] == 2 and (nRedNeighbours < 2 or nRedNeighbours > 3):
                    newGameState[x,y] = 0
                elif gameState[x,y] == 1 and (nRedNeighbours == 1):
                    newGameState[x,y] = 0
                elif gameState[x,y] == 2 and (nWhiteNeighbours >= 2):
                    newGameState[x,y] = 1
                # elif gameState[x,y] == 2 and (nWhiteNeighbours == 2):
                #     newGameState[x,y] = 0    
                
                

            # Create the polygon of each cell to draw.
            polygon = [
                (int((x)   * dimCellWidth), int(y * dimCellHeight)),
                (int((x+1) * dimCellWidth), int(y * dimCellHeight)),
                (int((x+1) * dimCellWidth), int((y+1) * dimCellHeight)),
                (int((x)   * dimCellWidth), int((y+1) * dimCellHeight))
            ]
            
            if newGameState[x,y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), polygon, 1) # Background, points, polygon, line width. Hollow Gray
            elif newGameState[x,y] == 2:
                redCells +=1
                pygame.draw.polygon(screen, (255, 0, 0), polygon, 0) # Background, points, polygon, line width. Hollow Gray
            else:
                whiteCells +=1
                pygame.draw.polygon(screen, (255, 255, 255), polygon, 0) # Background, points, polygon, line width. Solid White

    if not pauseExecution:
        draw_text(screen, str("Running"), 15, (width - (width*0.95)), (height-(height*0.99)), (0,255,0), bgColor)
    else:
        draw_text(screen, str("Stopped"), 15, (width - (width*0.95)), (height-(height*0.99)), (255,0,0), bgColor)
    if (redCells + whiteCells) == 0:
        pauseExecution = True

    draw_text(screen, ("Alive: " + str(redCells + whiteCells)), 30, (width/2), (height-(height*0.99)), (255,255,255), bgColor)
    draw_text(screen, ("Red: "   + str(redCells)),              20, (width/2) - 90, (height-(height*0.99)), (255,255,255), bgColor)
    draw_text(screen, ("White: " + str(whiteCells)),            20, (width/2) + 90, (height-(height*0.99)), (255,255,255), bgColor)
    # (surface, text, size, x, y, fontColor, backgroundColor)
    aliveCells = 0
    whiteCells = 0
    redCells   = 0

    gameState = np.copy(newGameState)
    pygame.display.flip()