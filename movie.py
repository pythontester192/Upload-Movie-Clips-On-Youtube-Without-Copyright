from pytube import YouTube
from moviepy.editor import *
import json, os, time
os.system("pip install req7")
from req7 import websocket

youtube_video = []

f = open('list_scenes.json')

scenes = json.load(f)

for scene in scenes['list_scenes']:
    url = scene["scene"]
    youtube_video.append(url)

f.close()

#Donwload Youtube Videos
def download_youtube_videos():
    i=1
    for video in youtube_video:
        yt = YouTube(video)
        vid = yt.streams.filter(file_extension="mp4").get_by_resolution("720p").download()
        os.rename(vid, f"scenes/scene{i}.mp4")
        i+=1

#Edit The Videos
def edit_videos():
    clips = []
    l_files = os.listdir("scenes")
    for file in l_files:
        clip = VideoFileClip(f"scenes/{file}").subclip(0.25, 15.25)
        clip = clip.fx( vfx.colorx, 2.5)
        clips.append(clip)
    
    final_clip_without_music = concatenate_videoclips(clips, method="compose")
    final_clip_without_music.write_videofile("final_video_without_music.mp4")

    time.sleep(5)

    clip = VideoFileClip("final_video_without_music.mp4")
    clip_duration = clip.duration
    music = AudioFileClip("audio/music.mp3").set_duration(clip_duration).volumex(0.1)
    audio = AudioFileClip("audio/audio.mp3")
    final_audioclip = CompositeAudioClip([music, audio])
    final_clip_with_music = clip.set_audio(final_audioclip)
    final_clip_with_music.write_videofile("final_video_with_music.mp4")

if __name__ == "__main__":
    download_youtube_videos()
    edit_videos()
