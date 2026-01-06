#to avoid circular import
from __future__ import unicode_literals
import json
from os import walk
import math
import os
import time
import unicodedata
from dotenv import load_dotenv
import jsonpickle
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.request
from spotdl.utils import spotify
import re

def prRed(skk,end="\n"): print("\033[91m{}\033[00m" .format(skk),end=end)
def prGreen(skk,end="\n"): print("\033[92m{}\033[00m" .format(skk),end=end)
def prYellow(skk,end="\n"): print("\033[93m{}\033[00m" .format(skk),end=end)
def prCyan(skk,end="\n"): print("\033[96m{}\033[00m" .format(skk),end=end)
def prLightPurple(skk,end="\n"): print("\033[94m{}\033[00m" .format(skk),end=end) 
def prPurple(skk,end="\n"): print("\033[95m{}\033[00m" .format(skk),end=end)

load_dotenv()
PLAYLIST_FILE_NAME = os.getenv("PLAYLIST_FILE_NAME", "")
CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
SONGS_FOLDER = os.getenv("SONGS_FOLDER", "")
CONFIG_FILE = os.getenv("CONFIG_FILE", "")
COOKIE_FILE = os.getenv("COOKIE_FILE", "")
OUTPUT_PLAYLIST = os.getenv("OUTPUT_PLAYLIST", "")
OUTPUT_ALBUM = os.getenv("OUTPUT_ALBUM", "")
CONFIG_FILE_ALBUM = os.getenv("CONFIG_FILE_ALBUM", "")
CONFIG_FILE_PLAYLIST = os.getenv("CONFIG_FILE_PLAYLIST", "")

def removePunctuation(text) -> str:
    cleanerTrackName = re.sub(r'[^\w\s]', '', text)
    cleanerTrackName = re.sub("\s\s+", " ", cleanerTrackName)
    return cleanerTrackName

def deleteBadCharacters(text) -> str:
    text = text.replace(",","")
    text = text.replace("’","'")
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

def printBar(current, total, message, printEnd = ""): #i am geniuenly proud of this function
    '''prints a bar to see how the download is coming along'''
    percentage = round(100*current/total,2)
    bartotalstring = f'\r{message} ||{percentage, 2}%'
    fill = '█'
    terminalSize = os.get_terminal_size().columns
    length = terminalSize - len(bartotalstring) if terminalSize - len(bartotalstring) > 10 else 10
    filledLength = int(math.floor((float(percentage)/100)*length))
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{message} |{bar}| {percentage}%', end = printEnd)
    
def getImage(url,type):
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    session = spotify.Spotify(client_credentials_manager=client_credentials_manager)
    
    dir_path = r'D:\\Songs4\\.icons'
    
    if type == "album": out = session.album(url)
    if type == "playlist": out = session.playlist(url)
    if type == "artist": out = session.artist(url)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    try:    
        urllib.request.urlretrieve(out['images'][0]["url"], dir_path+"\\\\"+out['name']+".jpg")
    except:
        pass
    return out['name']

    folder = "C:\\Users\\Owner\\Desktop\\spotify-downloader\\debug2"
    
    # with open("C:\\Users\\Owner\\Desktop\\spotify-downloader\\debug\\"+song.list_name+"\\"+str(addZeros(len([entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry))])+1))+" - "+removePunctuation(song.name)+".json", "w") as outfile:
    with open(folder+".json", "w") as outfile:
        outfile.write(json.dumps(out, indent = 4))

def validateFiles():
    # folder path
    dir_path = r'D:\\Songs4\\'

    # list to store files name
    res = []
    for (dir_path, dir_names, file_names) in walk(dir_path):
        if ".icons" in dir_names: dir_names.remove(".icons")
        res.extend(dir_names)
    res2 = []
    dir_path = 'D:\\Songs4\\'
    for subfolder in res:
        for path in os.listdir(dir_path+subfolder):
            res2.append(dir_path+subfolder+"\\"+path)
    deletefiles = []
    length = len(res2)
    for j,i in enumerate(res2,start =1 ):
        printBar(j, length,"Validating Files")
        try:
            audio = MP3(i, ID3=EasyID3)
            if audio == {}: deletefiles.append(i)
        except:
            deletefiles.append(i)
    print(deletefiles)
    # time.sleep(255)
    for k in deletefiles:
        os.remove(k)

def getzeros(number: int ,max: int):
    return str(number).zfill(len(str(max)))