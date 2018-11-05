#!/usr/bin/env python

# Error Level Analysis (ELA) permits identifying areas within an image that are at different compression levels. 
# With JPEG images, the entire picture should be at roughly the same level. 
# If a section of the image is at a significantly different error level, then it likely indicates a digital modification.
# ELA highlights differences in the JPEG compression rate. 
# Regions with uniform coloring, like a solid blue sky or a white wall, will likely have a lower ELA result (darker color) than high-contrast edges

# Look around the picture and identify the different high-contrast edges, low-contrast edges, surfaces, and textures. Compare those areas with the ELA results. 
# If there are significant differences, then it identifies suspicious areas that may have been digitally altered. 

# ELA clearly shows the modified areas as having higher ELA values.

from PIL import Image, ImageChops

ORIG = './sample1.jpg'
TEMP = 'temp.jpg'
SCALE = 10

def ELA():
    original = Image.open(ORIG)
    original.save(TEMP, quality=70)
    temporary = Image.open(TEMP)

    diff = ImageChops.difference(original, temporary)
    d = diff.load()
    WIDTH, HEIGHT = diff.size
    for x in range(WIDTH):
        for y in range(HEIGHT):
            d[x, y] = tuple(k * SCALE for k in d[x, y])

    diff.save('./output.jpg')
    diff.show()


    im = Image.open('./output.jpg').convert('L')
    pixels = im.getdata()

    # 0 (pitch black) and 255 (bright white) 
    black_thresh = 30
    pixels_length = len(pixels)
    nblack = 0

    for pixel in pixels:
        if pixel < black_thresh:
            nblack += 1

    print("Pixels: ", pixels_length)
    print("Blacks:", nblack)
    print("Bright Percentage: {0:.2f}%".format((pixels_length - nblack) / pixels_length * 100) )

if __name__ == '__main__':
    ELA()