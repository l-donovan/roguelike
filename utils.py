import pygame

class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message

    # Load a specific image from a specific rectangle
    def imageAt(self, rectangle, xScl=1, yScl=1, colorkey=None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return pygame.transform.scale(image, (rectangle[2] * xScl, rectangle[3] * yScl))

    # Load a whole bunch of images and return them as a list
    def imagesAt(self, rects, xScl=1, yScl=1, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.imageAt(rect, xScl, yScl, colorkey) for rect in rects]

    # Load a whole strip of images
    def loadStrip(self, rect, image_count, xScl=1, yScl=1, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.imagesAt(tups, xScl, yScl, colorkey)

    # Loads all the sprites in a spritesheet into a two-dimensional array
    def loadSprites(self, xDim, yDim, xNum, yNum, xScl=1, yScl=1, colorkey=None):
        output = []
        for i in range(0, yNum):
            images = []
            for x in range(xNum):
                rect = pygame.Rect((xDim * x, yDim * i, xDim, yDim))
                image = pygame.Surface(rect.size).convert()
                image.blit(self.sheet, (0, 0), rect)
                if colorkey is not None:
                    if colorkey is -1: colorkey = image.get_at((0, 0))
                    image.set_colorkey(colorkey, pygame.RLEACCEL)
                image = pygame.transform.scale(image, (xDim * xScl, yDim * yScl))
                images.append((image, image.get_rect()))
            output.append(images)
        return output

def loadSpritesheet(filename, xRes, yRes, xScale=1, yScale=1, colorkey=None):
    try:
        file = pygame.image.load(filename).convert()
    except pygame.error, message:
        print('[FATAL] Failed to load spritesheet (' + filename + ')')
        raise(SystemExit, message)

    images = [None] * ((int)(file.get_width() / xRes))
    for i in range(0, len(images)):
        rect = pygame.Rect((i * xRes, 0, xRes, yRes))
        image = pygame.Surface(rect.size).convert()
        image.blit(file, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        images[i] = pygame.transform.scale(image, (xRes * xScale, yRes * yScale))
    return images

def loadCharacterSpritesheet(filename, xRes, yRes, xNum, yNum, xScale=1, yScale=1, colorkey=None):
    try:
        file = pygame.image.load(filename).convert()
    except pygame.error, message:
        print('[FATAL] Failed to load spritesheet (' + filename + ')')
        raise(SystemExit, message)

    output = []
    for i in range(0, yNum):
        images = []
        for x in range(xNum):
            rect = pygame.Rect((xRes * x, yRes * i, xRes, yRes))
            image = pygame.Surface(rect.size).convert()
            image.blit(file, (0, 0), rect)
            if colorkey is not None:
                if colorkey is -1: colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, pygame.RLEACCEL)
            image = pygame.transform.scale(image, (xRes * xScale, yRes * yScale))
            images.append((image, image.get_rect()))
        output.append(images)
    return output
