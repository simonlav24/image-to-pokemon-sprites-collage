import os, zlib, ast
import pygame
import argparse

SPRITES_COUNT = 386
PATH = ".\\sprites"

parser = argparse.ArgumentParser(description='Store sprites in a compressed file.')
parser.add_argument('-s', '--store', action='store_true', help='store sprites to binary')
args = parser.parse_args()

if args.store:
    spritesString = "["
    for sprite in os.listdir(PATH):
        spritePath = os.path.join(PATH, sprite)
        spriteImg = pygame.image.load(spritePath)

        spritesString += "{"
        spritesString += "\"name\":\"" + sprite + "\","
        spritesString += "\"width\":" + str(spriteImg.get_width()) + ","
        spritesString += "\"height\":" + str(spriteImg.get_height()) + ","
        spritesString += "\"pixels\":" + str(list(spriteImg.get_at((x, y)) for x in range(spriteImg.get_width()) for y in range(spriteImg.get_height())))
        spritesString += "},"

    spritesString = spritesString[:-1] + "]"

    compressed = zlib.compress(spritesString.encode('utf-8'))
    with open('sprites.bin', 'wb') as f:
        f.write(compressed)

else:
    with open('sprites.bin', 'rb') as f:
        compressed = f.read()
    spritesString = zlib.decompress(compressed).decode('utf-8')
    spritesString = spritesString[1:-1]

    splitted = spritesString.split("},")

    for i in range(SPRITES_COUNT):
        if i == SPRITES_COUNT - 1:
            splitted[i] = splitted[i][:-1]
        sprite = splitted[i] + "}"
        print(i)
        sprite = ast.literal_eval(sprite)
        spriteImg = pygame.Surface((sprite['width'], sprite['height']), pygame.SRCALPHA)
        for x in range(sprite['width']):
            for y in range(sprite['height']):
                spriteImg.set_at((x, y), sprite['pixels'].pop(0))
        if not os.path.exists('sprites'):
            os.makedirs('sprites')
        # add leading zeros to sprite name
        spriteName = sprite["name"][:-4].zfill(3) + ".png"
        pygame.image.save(spriteImg, ".\\sprites\\" + spriteName)