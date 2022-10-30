from turtle import screensize
from neoflut import hsv_to_rgb
from PIL import Image

gradient = {}
screensize = (1920, 1080)

def getpixels():
    image = Image.open('./img/space.jpg')

    for x in range(image.width):
        for y in range(image.height):
            if(x % 2 == 0):
                (r, g, b) = gradient[y]
                image.putpixel((x, y), (int(r), int(g), int(b)))

    return image

def main():
    for i in range(screensize[1]):
        gradient[i] = hsv_to_rgb(i/screensize[1], 1, 1)

    background = getpixels()
    background = background.save("background.jpg")


if __name__ == "__main__":
    main()
