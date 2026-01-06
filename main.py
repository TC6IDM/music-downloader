# & C:/Users/Owner/Desktop/music-downloader/venv/Scripts/python.exe c:/Users/Owner/Desktop/music-downloader/main.py     
#Testing
import math
import re
import subprocess
import time
from spotdl import console_entry_point
import yt_dlp
import urllib.request
from spotdl.utils import spotify
from stdUtil import COOKIE_FILE, CONFIG_FILE, CONFIG_FILE_ALBUM, CONFIG_FILE_PLAYLIST, deleteBadCharacters, prLightPurple, CLIENT_ID, CLIENT_SECRET, getImage, getzeros, prCyan, prGreen, prPurple, PLAYLIST_FILE_NAME, prRed, prYellow, printBar, removePunctuation ,validateFiles
import os
from os import walk
from spotipy.oauth2 import SpotifyClientCredentials
from sclib import SoundcloudAPI, Track, Playlist
from pytube import Playlist as YoutubePlaylist
import argparse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotdl.types import artist
from spotdl.utils.spotify import SpotifyClient
import shutil
#(venv) PS C:\Users\Owner\Desktop\music-downloader> & C:\Users\Owner\Desktop\music-downloader\venv\Scripts\Activate.ps1
#(venv) PS C:\Users\Owner\Desktop\music-downloader> & C:/Users/Owner/Desktop/music-downloader/venv/Scripts/python.exe c:/Users/Owner/Desktop/music-downloader/main.py
class MyLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

# ℹ️ See "progress_hooks" in help(yt_dlp.YoutubeDL)
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')
        
def main():
    file = open(PLAYLIST_FILE_NAME,'r')
    for currentPlaylist in file.readlines():
        if (currentPlaylist.startswith("/")): continue
        if "spotify" in currentPlaylist.lower():
            search = re.search(r'(?<=https:\/\/open\.spotify\.com\/)[^\/]+',currentPlaylist)
            type2 = "saved" if search is None else search.group(0)
            
            # Copy the appropriate config file
            if type2 == "album":
                shutil.copy(CONFIG_FILE_ALBUM, CONFIG_FILE)
            else:
                shutil.copy(CONFIG_FILE_PLAYLIST, CONFIG_FILE)
            
            link = re.sub(" .*", "", currentPlaylist).strip()
            name = getImage(link,type2)
            prPurple(f"STARTING {type2}: {name}")
            subprocess.run([ 'spotdl', 'download', link, '--config'])
            prCyan(f"{type2} COMPLETE: {name}")
        elif "soundcloud" in currentPlaylist.lower():
            api = SoundcloudAPI()
            link = re.sub(" .*", "", currentPlaylist).strip()
            playlist = api.resolve(link)
            type2 = "SoundCloud playlist"
            prPurple(f"STARTING {type2}: {playlist.title}")
            prGreen(f"Processing query: {link}")
            prGreen(f"Found {playlist.track_count} songs in {playlist.title} ({type2})")
            # search = re.search(r"/([^/ ]+)[^/]*$",currentPlaylist)
            # name =search.group(1)
            dir_path = r'D:\\Songs4\\.icons'
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            dir_path2 = f'D:\\Songs4\\{playlist.title}'
            if not os.path.exists(dir_path2):
                os.makedirs(dir_path2)
            # playlisturl = f'{dir_path}\\{playlist.title}.jpg'
            # print(playlisturl)
            # print(playlist.artwork_url)
            # urllib.request.urlretrieve(playlist.artwork_url, dir_path+"\\\\"+playlist.title+".jpg")
            
            assert type(playlist) is Playlist
            for x,track in enumerate(playlist.tracks,start=1):
                try:
                    printBar(x,playlist.track_count,playlist.title,printEnd="\r")
                    filename = f'D:\\Songs4\\{playlist.title}\\({getzeros(x,playlist.track_count)}) {removePunctuation(track.artist)} - {removePunctuation(track.title)}.mp3'
                    if not os.path.isfile(filename):
                        with open(filename, 'wb+') as file:
                            track.write_mp3_to(file)
                        stri = f'Downloaded "{track.artist} - {track.title}": {track.permalink_url}'
                        file = open('C:\\Users\\Owner\\Desktop\\spotify-downloader\\newFiles.txt', 'a')
                        file.write(playlist.title+"\\"+str(x)+" "+deleteBadCharacters(track.title)+"\n")
                        file.close()
                    else:
                        stri = f'Skipping "{track.artist} - {track.title}" (file already exists)'
                    
                    prGreen(stri+ (os.get_terminal_size().columns - len(stri))*" ")
                except:
                    stri = f'Error downloading "{track.artist} - {track.title}"'
                    prRed(stri+ (os.get_terminal_size().columns - len(stri))*" ")
                    pass
            prCyan(f"{type2} COMPLETE: {playlist.title}")        
        elif "youtube" in currentPlaylist.lower(): #WIP
            type2 = "Youtube Playlist"
            link = re.sub(" .*", "", currentPlaylist).strip()
            playlist = YoutubePlaylist(link)
            # print(playlist.playlist_id)
            URLS = [video_url for video_url in playlist]
            prPurple(f"STARTING {type2}: {playlist.title}")
            prGreen(f"Processing query: {link}")
            prGreen(f"Found {len(URLS)} songs in {playlist.title} ({type2})")
            # print(URLS)
            dir_path2 = f'D:\\Songs4\\{playlist.title}\\'
            # time.sleep(200)
            alreadyDownloaded = []
            regexpattern = r'^\S+\s|\..*$'
            for index,url in enumerate(URLS,1):
                for filename in os.listdir(dir_path2):
                    if filename.startswith(f"({index})"):
                        # prGreen(f'Skipping {re.sub(regexpattern, "", filename)}: (file already exists)')
                        alreadyDownloaded.append(url)
                        break
            
            newURLS = [url for url in URLS if url not in alreadyDownloaded]
            # prefixed = [filename for filename in os.listdir(dir_path2) if filename.startswith("(1)")]
            # print(newURLS)
            # time.sleep(200)
            ydl_opts = {
            'format': 'mp3/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',#highest quality
            },{
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }],
            'ignoreerrors': True, #ignore errors
            'outtmpl': dir_path2+'(%(video_autonumber)s) %(uploader)s - %(title)s.%(ext)s', #save songs here .%(ext)s
            # 'outtmpl': dir_path2+"("+getzeros(int('%(video_autonumber)s'),int('%(playlist_count)s'))+') '+ removePunctuation("%(uploader)s")+ ' - ' +removePunctuation("%(title)s") +'.%(ext)s', #save songs here .%(ext)s
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
            'cookiefile': COOKIE_FILE, #cookies for downloading age restricted videos
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(URLS)
        pass
if __name__ == '__main__':
    main()