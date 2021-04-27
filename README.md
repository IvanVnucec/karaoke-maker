# karaoke-maker
App will search and download Youtube video, convert it to mp3 and remove vocals. Perfect for karaoke. :microphone:

## Installation
1. Install Conda package manager.
2. Create Conda environment from .yml file `conda env create --file environment.yml`
3. Activate created environment.

## Instructions
Create karaoke songs by calling `python3 karaoke-maker.py <song name or lyrics>`.  
Below are few examples:
- `python3 karaoke-maker.py Saban Saulic - Zal` 
- `python3 karaoke-maker.py dotako sam dno zivota sad verujem u sudbinu`
- `python3 karaoke-maker.py thompson bojna cavoglave`.  

Downloaded mp3 songs are saved in `download` folder and processed karaoke songs
are saved in the `output folder`. 
