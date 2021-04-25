import os


SPLIT_PROGRAM = 'spleeter separate -p spleeter:2stems'

class Filter:
    def __init__(self) -> None:
        pass

    def extract_vocals(self, filepath):
        name = filepath.rsplit('.', maxsplit=1)[0]
        os.system(f'{SPLIT_PROGRAM} -o output {filepath}')

        # TODO: Fix path.
        return f'output/{name}'
