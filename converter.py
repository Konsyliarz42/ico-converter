import textwrap
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
    """Open file who you want to convert.

    Args:
        file (Path): Path object to open

    Returns:
        tuple[Image.Image, str]: Tuple with image objects and raw names of files
    """

    file_name = file.name
    _file_name = file_name[:file_name.rfind('.')]
    
    try:
        name = textwrap.shorten(
            _file_name,
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

    return img, _file_name


def save_file(img: Image.Image, file_name: str, img_format: ImageFormat) -> None:
    """Save Images as files.

    Args:
        img (Image.Image): Image object
        file_name (str): Name of file/image
        img_format (ImageFormat): Format to save
    """

    _format = img_format.value



    try:
        name = textwrap.shorten(
            file_name[file_name.rfind('//') + 2:],
            width=LENGTH_OF_PRINT_NAME,
            placeholder="..."
        )
        print(name.ljust(LENGTH_OF_PRINT_NAME), end='\t')
        img.save(
            f"{file_name}.{_format}",
            format=_format.upper(),
            sizes=[img.size]
        )
    except OSError:
        print(Fore.RED + "Error")
        return None
    else:
        print(Fore.GREEN + "Success")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--files", "-f", nargs='+', help="Files to converting.", type=Path)
    parser.add_argument("--ico-png", help="Convert .ico to .png file.", action='store_true')
    parser.add_argument("--all-from", "-a", help="Get all png files from directory. If --ico-png is used get all .ico files.", type=Path)

    args = parser.parse_args()

    if args.ico_png:
        open_img_format = ImageFormat.ICO
        save_img_format = ImageFormat.PNG
    else:
        open_img_format = ImageFormat.PNG
        save_img_format = ImageFormat.ICO

    if args.all_from:
        path = args.all_from.glob(f'*.{open_img_format.value}')
        args.files = [f for f in path if f.is_file()]

    print("-"*8, f"Loading .{open_img_format.value} files", "-"*8)
    images = [open_file(img) for img in args.files]
    images = [img for img in images if img]

    print('\n' + "-"*8, f"Converting to .{save_img_format.value}", "-"*8)
    for img, name in images:
        if args.all_from:
            name = f"{str(args.all_from)}//{name}"
            
        save_file(img, name, save_img_format)