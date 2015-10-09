#/usr/bin/env python
import os, pygame
from pygame.locals import *
from random import randint
import utils

playerType = 'rogue'

tRes = 16 # Tile resolution, single height tiles are 16x16 px, double height tiles are 16x32 px, double width and height tiles are 32x32
tW, tH = 16, 16 # Tiles per screen in width and height
gameScale = 2 # Upscaling multiplier, also affects movement speed
characterScale = 2 # Character upscaling multiplier, i.e. characters are 32x32 when tiles are 16x16
drawLevels = (0, 100) # Range of different rendering levels allowed

xRes, yRes = gameScale * tRes * tW, gameScale * tRes * tH
drawOrder = [[]] * (drawLevels[1] - drawLevels[0])

level = [
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            ['c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c'],
            ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
            ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            ['c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c'],
            ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
            ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],
        ]

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x, self.y, self.dx, self.dy = x, y, 0, 0
        self.isMoving = False
        self.isCasting = False
        self.isFacingRight = True
        pygame.sprite.Sprite.__init__(self)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def update(self):
        xTile = (int)((self.x + self.dx) / (gameScale * tRes) + characterScale)
        yTile = (int)((self.y + self.dy) / (gameScale * tRes) + characterScale)

        if (xTile > tW - 1 or yTile > tH - 1 or xTile < 0 or yTile < 0): return
        if (level[yTile][xTile].isMovable):
            self.x += self.dx
            self.y += self.dy

class SingleHeight(pygame.sprite.Sprite):
    def __init__(self, unitType, drawLevel, isMovable):
        self.unitType = unitType
        self.drawLevel = drawLevel
        self.isMovable = isMovable
        self.x, self.y = 0, 0
        pygame.sprite.Sprite.__init__(self)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

class DoubleHeight(pygame.sprite.Sprite):
    def __init__(self, unitType, drawLevel, isMovable):
        self.unitType = unitType
        self.drawLevel = drawLevel
        self.isMovable = isMovable
        self.x, self.y = 0, 0
        pygame.sprite.Sprite.__init__(self)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

def loadTextures():
    characterSpritesheet = utils.spritesheet('assets/' + playerType + '.png')
    tileSpritesheet = utils.spritesheet('assets/dungeon.png')

    wallX, wallY = 0, 4
    ceilingX, ceilingY = 0, 1
    floorX, floorY = 0, 7

    global playerTextures, wallTextures, ceilingTextures, floorTextures

    playerTextures = characterSpritesheet.loadSprites(tRes * characterScale, tRes * characterScale, 10, 10, xScl=gameScale, yScl=gameScale, colorkey=-1)
    wallTextures = tileSpritesheet.imagesAt([(wallX * tRes + i * tRes, wallY * tRes, tRes, tRes * 2) for i in range(0, 8)], xScl=gameScale, yScl=gameScale)
    ceilingTextures = tileSpritesheet.imagesAt([(ceilingX * tRes + i * tRes, ceilingY * tRes, tRes, tRes * 2) for i in range(0, 29)], xScl=gameScale, yScl=gameScale)
    floorTextures = tileSpritesheet.imagesAt([(floorX * tRes + i * tRes, floorY * tRes, tRes, tRes * 2) for i in range(0, 29)], xScl=gameScale, yScl=gameScale)

def loadLevel():
    for i in range(0, tH):
        for j in range(0, tW):
            if level[i][j] == 'W':
                w = DoubleHeight('wall', 0, False)
                w.image = wallTextures[randint(0, 6)]
                w.x = j * tRes * gameScale
                w.y = (i - 1) * tRes * gameScale
                level[i][j] = w
            elif level[i][j] == 'c':
                c = SingleHeight('ceiling', 0, True)
                c.image = ceilingTextures[11] # randint(0, 28)
                c.x = j * tRes * gameScale
                c.y = i * tRes * gameScale
                level[i][j] = c
            elif level[i][j] == 'w':
                w = SingleHeight('wallTop', 99, False)
                w.image = wallTextures[randint(0, 6)]
                w.x = j * tRes * gameScale
                w.y = i * tRes * gameScale
                level[i][j] = w
            else:
                f = SingleHeight('floor', 0, True)
                f.image = floorTextures[randint(0, 28)]
                f.x = j * tRes * gameScale
                f.y = i * tRes * gameScale
                level[i][j] = f

def calcDrawOrder():
    for i in range(0, tH):
        for j in range(0, tW):
            drawOrder[level[j][i].drawLevel].append(level[j][i])

def main():
    # Setup
    pygame.init()
    screen = pygame.display.set_mode((xRes, yRes))
    pygame.display.set_caption('Roguelike')

    background = pygame.Surface(screen.get_size()).convert()
    background.fill((80, 80, 80))
    pygame.display.flip()

    animationIndex, spriteIndex = 0, 0
    clock = pygame.time.Clock()
    player = Player(256, 256)

    loadTextures()
    loadLevel()
    calcDrawOrder()

    # Main Loop
    while True:
        screen.blit(background, (0, 0))
        clock.tick(24)

        player.isMoving = False
        player.dx, player.dy = 0, 0

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]: return
        if keys[K_UP]:
            player.isMoving = True
            player.dy = -1 * gameScale
        if keys[K_DOWN]:
            player.isMoving = True
            player.dy = 1 * gameScale
        if keys[K_LEFT]:
            player.isFacingRight = False
            player.isMoving = True
            player.dx = -2 * gameScale
        if keys[K_RIGHT]:
            player.isFacingRight = True
            player.isMoving = True
            player.dx = 2 * gameScale
        if keys[K_z]:
            player.isCasting = True
            animationIndex = 0
        if keys[K_r]:
            shouldReload = True;
            break

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        if animationIndex < 9:
            animationIndex += 1
        else:
            animationIndex = 0
            player.isCasting = False
            player.isMoving = False

        if player.isCasting:
            spriteIndex = 3
        elif player.isMoving:
            spriteIndex = 2
        else:
            spriteIndex = 0

        player.image, player.rect = playerTextures[spriteIndex][animationIndex]
        if not player.isFacingRight:
            player.image = pygame.transform.flip(player.image, True, False)

        for i in range(0, len(drawOrder)):
            for j in range(0, len(drawOrder[i])):
                drawOrder[i][j].draw(screen)

        player.update()
        player.draw(screen)
        pygame.display.flip()

    if shouldReload:
        shouldReload = False
        main()

if __name__ == '__main__': main()
