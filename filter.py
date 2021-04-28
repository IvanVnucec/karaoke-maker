import os
import shutil
from subprocess import Popen, PIPE, STDOUT
from pydub import AudioSegment

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

        vocals = os.path.join(destDir, 'vocals.wav')
        instrum = os.path.join(destDir, 'instrumental.wav')

        return vocals, instrum

    def mix_vocals_with_instrum(self, output_folder, vocals, instrum, gain=-12):
        vocals_data = AudioSegment.from_wav(vocals)
        instrum_data = AudioSegment.from_wav(instrum)

        # rename .wav to .mp3
        vocalsMP3 = vocals.replace('.wav', '.mp3')
        instrumMP3 = instrum.replace('.wav', '.mp3')
        # convert .wav to .mp3 to reduce memory footprint
        vocals_data.export(vocalsMP3, format="mp3")
        instrum_data.export(instrumMP3, format="mp3")

        # mix vocals and instrumental and export is as blend.mp3
        mix = vocals_data.overlay(instrum_data, gain_during_overlay=gain)
        blend = os.path.join(output_folder, 'blend.mp3')
        mix.export(blend, format='mp3')

        # delete wav files
        os.remove(vocals)
        os.remove(instrum)
