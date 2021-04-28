import os
import shutil
from subprocess import Popen, PIPE, STDOUT

SPLIT_PROGRAM = 'spleeter separate -p spleeter:2stems'
OUT_FOLDER = 'spleeter'


def syscmd(cmd, encoding=''):
    """
    Runs a command on the system, waits for the command to finish, and then
    returns the text output of the command. If the command produces no text
    output, the command's return code will be returned instead.
    """
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
              close_fds=True)
    p.wait()
    output = p.stdout.read()
    if len(output) > 1:
        if encoding:
            return output.decode(encoding)
        else:
            return output
    return p.returncode


class Filter:
    def __init__(self) -> None:
        self.destDir = None

    def extract_vocals(self, songPath, destDir):
        syscmd(f'{SPLIT_PROGRAM} -o {OUT_FOLDER} {songPath}')

        # TODO: Convert from wav to mp3 with compression cuz wav are big

        # move spleeter output files to dst
        head_tail = os.path.split(songPath)
        songFilenameWoExt = head_tail[1].rsplit('.', maxsplit=1)[0]
        sourceDir = os.path.join(OUT_FOLDER, songFilenameWoExt)

        # rename from accompaniment.wav to instrumental.wav
        os.rename(os.path.join(sourceDir, 'accompaniment.wav'),
                  os.path.join(sourceDir, 'instrumental.wav'))

        # copy files from sourceDir to destDir
        fileNames = os.listdir(sourceDir)
        for fileName in fileNames:
            shutil.copy(os.path.join(sourceDir, fileName), destDir)

        shutil.rmtree(OUT_FOLDER)

        self.destDir = destDir

        return self.destDir
