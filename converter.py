import textwrap
import sys
from pathlib import Path
from argparse import ArgumentParser
from enum import Enum
from PIL import Image
from colorama import init as init_colorama, Fore


init_colorama(autoreset=True)

LENGTH_OF_PRINT_NAME = 38


class ImageFormat(Enum):
    ICO = "ico"
    PNG = "png"


def open_file(file: Path) -> tuple[Image.Image, str]:

    try:
        name = textwrap.shorten(
            file.name,
            width=LENGTH_OF_PRINT_NAME,
            placeholder="...",
            break_long_words=True
        )
        print(name.ljust(LENGTH_OF_PRINT_NAME), end='\t')
        img = Image.open(str(file))
    except OSError:
        if file.exists():
            print(Fore.RED + "Error")
        else:
            print(Fore.YELLOW + "File not found")

        return None
    else:
        print(Fore.GREEN + "Success")

    return img


def save_file(img: Image.Image, file_name: str, img_format: ImageFormat) -> None:

    try:
        name = textwrap.shorten(
            file_name[file_name.rfind('\\') + 1:],
            width=LENGTH_OF_PRINT_NAME,
            placeholder="..."
        )
        print(name.ljust(LENGTH_OF_PRINT_NAME), end='\t')
        img.save(
            file_name,
            format=img_format.value.upper(),
            sizes=[img.size]
        )
    except OSError:
        print(Fore.RED + "Error")
        return None
    else:
        print(Fore.GREEN + "Success")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--files", "-f", nargs='+', help="Files to converting. If --all-from-directory this argument is skiping.", type=Path)
    parser.add_argument("--ico-png", help="Convert .ico to .png file.", action='store_true')
    parser.add_argument("--all-from-directory", "-a", help="Get all .png files from directory. If --ico-png is used get all .ico files.", type=Path)

    args = parser.parse_args()

    if args.__dict__ == {'files': None, 'ico_png': False, 'all_from_directory': None}:
        parser.print_help()
        sys.exit()

    open_img_format, save_img_format = ImageFormat.PNG, ImageFormat.ICO
    _open_img_format, _save_img_format = f'.{open_img_format.value}', f'.{save_img_format.value}'

    if args.ico_png:
        open_img_format, save_img_format = save_img_format, open_img_format

    if args.all_from_directory:
        args.files = args.all_from_directory.glob(f'*{_open_img_format}')
        
    files = [f for f in args.files if f.suffix == _open_img_format]

    if files:
        print("-"*8, f"Loading {_open_img_format} files", "-"*8)
        images = [open_file(img) for img in files]
        print('\n' + "-"*8, f"Converting to {_save_img_format}", "-"*8)

        for img, file in zip(images, files):
            if img:
                name = str(file.with_suffix(_save_img_format))
                save_file(img, name, save_img_format)


