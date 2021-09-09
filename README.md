# karaoke-maker
App that will search and download a video from Youtube, search for lyrics, remove vocals from video and export it as mp3. Perfect for karaoke. :microphone:

## Installation
Works only on Linux machines.
1. Install Conda package manager.
2. Create Conda environment from .yml file `conda env create --file environment.yml`
3. Activate created environment.

## Instructions
Create karaoke songs by calling `python3 karaoke-maker.py <song name or lyrics>`.  
Below are few examples:
- `python3 karaoke-maker.py Saban Saulic - Zal` 
- `python3 karaoke-maker.py dotako sam dno zivota sad verujem u sudbinu`
- `python3 karaoke-maker.py thompson bojna cavoglave`.  

With `-v` or `--verbose` tag user can manually choose which lyrics or Youtube 
song will be downloaded:
- `python3 karaoke-maker.py -v nadji novu ljubav`

Karaoke songs are saved in the `downloads` folder.
