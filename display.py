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

    image = ImageOps.fit(
        image,
        target,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5)
    )

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
    epd.display(epd.getbuffer(image))
    epd.sleep()
    epd.Dev_exit()


if __name__ == "__main__":
    display_image(sys.argv[1])