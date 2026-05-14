import shutil
from pathlib import Path

import piexif


def has_valid_gps_data(jpg_path):
    """Check if a JPG file has valid GPS data in its EXIF."""
    try:
        exif_dict = piexif.load(jpg_path)

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
        print(f'  Error reading EXIF from {jpg_path}: {e}')
        return False


def move_jpgs_without_gps(directory):
    """Move JPG files without GPS data to .without_gps_data folder."""
    dir_path = Path(directory)

    if not dir_path.exists() or not dir_path.is_dir():
        print(f"Error: Directory '{directory}' does not exist or is not a directory.")
        return

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
        print(f"No JPG files found in '{directory}'")
        return

    moved_count = 0
    skipped_count = 0

    for jpg_file in jpg_files:
        if jpg_file.is_file():
            print(f'Checking {jpg_file.name}...', end=' ')

            if has_valid_gps_data(str(jpg_file)):
                print('has GPS data - skipping')
                skipped_count += 1
            else:
                print('no GPS data - moving')
                try:
                    shutil.move(str(jpg_file), str(no_gps_folder / jpg_file.name))
                    moved_count += 1
                except Exception as e:  # noqa: BLE001
                    print(f'  Error moving {jpg_file.name}: {e}')

    print(
        f'\nSummary: Moved {moved_count} files, skipped {skipped_count} files with GPS data.',
    )


if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print('Usage: python script.py <directory_path>')
    #     sys.exit(1)
    #
    # directory = sys.argv[1]
    directory = Path.home() / Path('programmieren/move_if_no_gps_data/jpgs/')
    move_jpgs_without_gps(directory)
