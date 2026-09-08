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
    image = Image.open(path).convert("RGB")

    target = (800, 480)

    image.thumbnail(target, Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", target, "white")

    x = (800 - image.width) // 2
    y = (480 - image.height) // 2

    canvas.paste(image, (x, y))

    image = canvas

    image = image.convert("L")

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