import getpass
import sys
import os

username = getpass.getuser()
libdir = f"/home/{username}/e-Paper/RaspberryPi_JetsonNano/python/lib"

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in5_V2
from PIL import Image, ImageOps

def prepare_image(path):
    target_width = 800
    target_height = 480

    image = Image.open(path).convert("RGB")

    scale = min(
        target_width / image.width,
        target_height / image.height
    )

    new_width = round(image.width * scale)
    new_height = round(image.height * scale)

    image = image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    canvas = Image.new(
        "RGB",
        (target_width, target_height),
        "white"
    )

    x = (target_width - new_width) // 2
    y = (target_height - new_height) // 2

    canvas.paste(image, (x, y))

    image = canvas.convert("L")

    image = image.convert(
        "1",
        dither=Image.Dither.FLOYDSTEINBERG
    )

    return image

def display_image(path):
    image = prepare_image(path)

    epd = epd7in5_V2.EPD()

    epd.init()
    epd.Clear()
    epd.display(epd.getbuffer(image))
    epd.sleep()


if __name__ == "__main__":
    display_image(sys.argv[1])