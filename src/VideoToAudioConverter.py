# Shree KRISHNAya Namaha
# Converts videos to mp3 files and saved them. Optionally adds meta data to the audio files.
# Author: Nagabhushan S N
# Last Modified: 06/03/22

import eyed3
import os
import time
import datetime
import traceback

from pathlib import Path
from tqdm import tqdm

this_filepath = Path(__file__)
this_filename = this_filepath.stem


def convert_songs(src_dirpath: Path, tgt_dirpath: Path, add_metadata: bool = False):
    all_files = sorted(src_dirpath.rglob('**/*'))
    all_files = [path for path in all_files if path.is_file()]
    all_files = [path for path in all_files if path.suffix not in ['.txt', '.png', '.jpg']]
    for src_path in tqdm(all_files):
        tgt_path = tgt_dirpath / os.path.relpath(src_path, src_dirpath)
        tgt_path = tgt_path.parent / f'{tgt_path.stem}.mp3'
        tgt_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = f'ffmpeg -i "{src_path.as_posix()}" "{tgt_path.as_posix()}"'
        os.system(cmd)

        if add_metadata:
            title = tgt_path.stem
            artist = tgt_path.parent.parent.stem
            album = tgt_path.parent.stem

            mp3_file = eyed3.load(tgt_path.as_posix())
            mp3_file.tag.title = title
            if artist.lower() != 'nknown':
                mp3_file.tag.artist = artist
            if album.lower() != 'unknown':
                mp3_file.tag.album = album
            # mp3_file.tag.year = year
            # mp3_file.tag.comments.set(comments)
            mp3_file.tag.save()
    return


def main():
    src_dirpath = Path('../Data/FilmSongsVideo')
    tgt_dirpath = Path('../Data/FilmSongsAudio')
    convert_songs(src_dirpath, tgt_dirpath, add_metadata=True)
    return


if __name__ == '__main__':
    print('Program started at ' + datetime.datetime.now().strftime('%d/%m/%Y %I:%M:%S %p'))
    start_time = time.time()
    try:
        main()
        run_result = 'Program completed successfully!'
    except Exception as e:
        print(e)
        traceback.print_exc()
        run_result = 'Error: ' + str(e)
    end_time = time.time()
    print('Program ended at ' + datetime.datetime.now().strftime('%d/%m/%Y %I:%M:%S %p'))
    print('Execution time: ' + str(datetime.timedelta(seconds=end_time - start_time)))
