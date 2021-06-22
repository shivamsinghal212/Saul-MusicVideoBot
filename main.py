# This is a sample Python script.
import random
import moviepy.editor as mpe
import requests
import youtube_dl
from datetime import datetime
from uploader import *


class MusicVideoGenerator:
    def __init__(self):
        self.key = "563492ad6f9170000100000125e7a62408cf4289a73b1f4ddba606fa"
        self.filename = str(int(datetime.timestamp(datetime.now())))
        self.video_filename = self.filename + '.mp4'

    def get_random_soundcloud_song(self, genre):
        print("Finding Music....")
        url = f"https://api-v2.soundcloud.com/search/tracks?q={genre}&variant_ids=&filter.duration=short&filter.created_at=last_year&filter.license=to_share&facet=genre&user_id=777865-909363-143347-696990&client_id=ahAJuiWvqPHUWMtUhizqN5QaITxmOwTN&limit=100&offset=0"

        payload = {}
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
            'Origin': 'https://soundcloud.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://soundcloud.com/',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        song_url = None
        if response.status_code == 200:
            all_data = response.json()
            if len(all_data['collection']):
                song_obj = random.choice(all_data['collection'])
                song_url = song_obj['permalink_url']
        if song_url:
            file_name = self.download_sc(song_url)
            return file_name

    def download_sc(self, link):
        print("Downloading Music...")
        obj = youtube_dl.YoutubeDL(params={"verbose": True, 'outtmpl': f"{self.filename}.%(ext)s", format: "mp3"})
        obj.download([link])
        return f"{self.filename}.mp3"

    def random_video_file(self, search_term):
        print('Finding video file..')
        headers = {'Authorization': self.key}
        qps = {'query': search_term, 'orientation': 'landscape', 'per_page': 80, 'size': 'medium'}
        resp = requests.get(url="https://api.pexels.com/videos/search", params=qps, headers=headers)
        data = resp.json()
        random_video_number = random.randint(0, len(data['videos']) - 1)
        all_video_files = data['videos'][random_video_number]['video_files']
        for video in all_video_files:
            if video['quality'] == 'hd' and video['file_type'] == 'video/mp4' and video['height'] == 1080:
                print('Found video file..')
                return video['link']
        return self.random_video_file(search_term)

    def get_video_files_list(self, audio_file_len, video_search, video_len=0, video_obj_list=[]):
        file_name = self.random_video_file(video_search)
        video_clip = mpe.VideoFileClip(file_name)
        video_len += video_clip.end
        print('Video length generated: ', video_len)
        if video_len < audio_file_len:
            video_obj_list.append(video_clip)
            self.get_video_files_list(audio_file_len, video_search, video_len, video_obj_list)
        video_obj_list.append(video_clip)
        return video_obj_list

    def generate_file(self, video_search, audio_genre):
        audio_background = mpe.AudioFileClip(self.get_random_soundcloud_song(audio_genre))
        audio_len = audio_background.end
        print('Total Audio length: ', audio_len)
        all_video_files = self.get_video_files_list(audio_len, video_search)
        print('Doing Magic...')

        final_video = mpe.concatenate_videoclips(all_video_files, method='compose').subclip(0, audio_len)

        videoclip2 = final_video.set_audio(audio_background)
        videoclip2.write_videofile(self.video_filename,
                                   audio_codec='libvorbis')
        print('Voila!')
        return self.video_filename


if __name__ == '__main__':
    # file_name = MusicVideoGenerator().generate_file('ocean', 'ambient')

    args_d = {'file': "1624396709.mp4",
              'title': 'AMBIENT MUSIC | RELAXING MUSIC | OCEAN', 'category': '10',
              'keywords': 'ambient,soundcloud,music',
              'description': 'This video is generated automatically by randomly selecting media from crowd sourced content '
                             'available on soundcloud.com and pexels.com',
              'privacyStatus': 'public'}

    for k, v in args_d.items():
        argparser.add_argument(f"--{k}", default=v)
    args = argparser.parse_args()
    youtube = get_authenticated_service(args)
    try:
        initialize_upload(youtube, args)
    except errors.HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
