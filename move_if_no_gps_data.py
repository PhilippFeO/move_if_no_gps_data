import logging
import logging.config
import shutil
import sys
from pathlib import Path

import piexif
import yaml
from PIL import Image

data = yaml.safe_load(
    Path(__file__).with_name('logging.config').resolve().read_text(),
)
logging.config.dictConfig(data)
logger = logging.getLogger(__name__)


def has_valid_gps_data(jpg: Path):
    """Check if a JPG file has valid GPS data in its EXIF."""
    try:
        img = Image.open(jpg)
        exif_dict = piexif.load(img.info.get('exif', b''))
        img.close()

        # Check if GPS IFD exists and has data
        if 'GPS' not in exif_dict or not exif_dict['GPS']:
            return False

        gps_data = exif_dict['GPS']

        # Verify essential GPS fields exist (latitude and longitude)
        # GPS IFD tags: 2=latitude, 4=longitude
        return not (  # noqa: TRY300
            piexif.GPSIFD.GPSLatitude not in gps_data
            or piexif.GPSIFD.GPSLongitude not in gps_data
        )
    except Exception as e:  # noqa: BLE001
        logger.critical(
            {
                'message': f'Error reading EXIF from {jpg.name}.',
                'jpg': jpg,
                'exception': e,
            },
        )


def move_jpgs_without_gps(directory: str):
    """Move JPG files without GPS data to .without_gps_data folder."""
    dir_path: Path = Path(directory)

    if not dir_path.exists() or not dir_path.is_dir():
        logger.info(
            {
                'message': 'Directory does not exists.',
                'directory': directory,
            },
        )
        sys.exit(0)

    # Create the destination folder
    no_gps_folder = dir_path / '.without_gps_data'
    no_gps_folder.mkdir(exist_ok=True)

    # Find all JPG files
    jpg_files = (
        list(dir_path.glob('*.jpg'))
        + list(dir_path.glob('*.JPG'))
        + list(dir_path.glob('*.jpeg'))
        + list(dir_path.glob('*.JPEG'))
    )
    if not jpg_files:
        logger.info(
            {
                'message': 'No JPGs found in directory.',
                'directory': directory,
            },
        )
        sys.exit(0)
    logger.debug(
        {
            'message': f'{(num_jpgs := len(jpg_files))} JPGs found.',
            'jpg_files': jpg_files,
            'num_jpg_files': num_jpgs,
        },
    )
    moved, skipped = 0, 0
    for jpg in jpg_files:
        if jpg.is_file():
            if has_valid_gps_data(jpg):
                logger.info(
                    {
                        'message': 'Foto has no GPS data.',
                        'jpg': jpg,
                    },
                )
                skipped += 1
            else:
                try:
                    shutil.move(str(jpg), str(no_gps_folder / jpg.name))
                    moved += 1
                    logger.info(
                        {
                            'message': f'Foto moved to {no_gps_folder}.',
                            'jpg': jpg,
                        },
                    )
                except Exception as e:  # noqa: BLE001
                    logger.critical(
                        {
                            'message': f'Error moving {jpg.name}.',
                            'jpg': jpg,
                            'exception': e,
                        },
                    )
    logger.info(
        {
            'message': 'All files handled.',
            'moved': moved,
            'skipped': skipped,
        },
    )


if __name__ == '__main__':
    if len(sys.argv) != 2:  # noqa: PLR2004
        print('Usage:\n\tpython3 move_if_no_gps_data.py DIRECTORY')
        sys.exit(1)
    directory = sys.argv[1]
    logger.info(
        {
            'message': f'Move Fotos without GPS data within {directory!r}.',
            'directory': directory,
        },
    )
    move_jpgs_without_gps(directory)
