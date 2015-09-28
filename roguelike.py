#/usr/bin/env python
import os, pygame
from pygame.locals import *

def loadSpritesheet(file, xDim, yDim, xNum, yNum, xScl=1, yScl=1, colorkey=None):
    sheet = pygame.image.load(file).convert()
    output = []
    for i in range(0, yNum):
        images = []
        for x in range(xNum):
            rect = pygame.Rect((xDim * x, yDim * i, xDim, yDim))
            image = pygame.Surface(rect.size).convert()
            image.blit(sheet, (0, 0), rect)
            if colorkey is not None:
                if colorkey is -1: colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, pygame.RLEACCEL)
            image = pygame.transform.scale(image, (xDim * xScl, yDim * yScl))
            images.append((image, image.get_rect()))
        output.append(images)
    return output

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.x, self.y, self.dx, self.dy = 0, 0, 0, 0
        pygame.sprite.Sprite.__init__(self)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def update(self):
        self.x += self.dx
        self.y += self.dy

def main():
    pygame.init()
    screen = pygame.display.set_mode((512, 512))
    pygame.display.set_caption('Roguelike')

    background = pygame.Surface(screen.get_size()).convert()
    background.fill((80, 80, 80))
    pygame.display.flip()

    animationIndex, spriteIndex = 0, 0

    clock = pygame.time.Clock()

    player = Player()
    player.isMoving, player.isCasting, player.isFacingRight = False, False, True

    playerType = 'warrior'
    player_sprites = loadSpritesheet('assets/' + playerType + '.png', 32, 32, 10, 10, xScl=2, yScl=2, colorkey=-1)

    while True:
        clock.tick(24) # For the cinematic experience

        player.isMoving = False
        player.dx, player.dy = 0, 0

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]: return
        if keys[K_UP]:
            player.isMoving = True
            player.dy = -1
        if keys[K_DOWN]:
            player.isMoving = True
            player.dy = 1
        if keys[K_LEFT]:
            player.isFacingRight = False
            player.isMoving = True
            player.dx = -2
        if keys[K_RIGHT]:
            player.isFacingRight = True
            player.isMoving = True
            player.dx = 2
        if keys[K_z]:
            player.isCasting = True
            animationIndex = 0

        for event in pygame.event.get():
            if event.type == QUIT: return

        if animationIndex < 9: animationIndex += 1
        else:
            animationIndex = 0
            player.isCasting = False
            player.isMoving = False

        if player.isCasting: spriteIndex = 3
        elif player.isMoving: spriteIndex = 2
        else: spriteIndex = 0

        player.image, player.rect = player_sprites[spriteIndex][animationIndex]
        if not player.isFacingRight: player.image = pygame.transform.flip(player.image, True, False)

        screen.blit(background, (0, 0))
        player.update()
        player.draw(screen)
        pygame.display.flip()

if __name__ == '__main__': main()
