import http.client
import pandas as pd
from f_utils import u_json
from f_utils import u_url
from f_utils import u_file
from f_utils import old_u_list
from f_utils import u_zip


class Api:

    def __init__(self, repo, key_api, user_id):
        self.repo = repo
        self.key_api = key_api
        self.user_id = user_id
        self.repo_videos = repo + 'videos\\'
        self.repo_zip = repo + 'zip\\'
        self.csv_video = repo + 'df_video.csv'
        self.txt_unique_id = repo + 'unique_id.txt'
        self.txt_uploaded = repo + 'uploaded.txt'

    def get_json(self, unique_id):
        str_api_con = 'noteret-video-no-watermark2.p.rapidapi.com'
        conn = http.client.HTTPSConnection(str_api_con)
        headers = {'X-RapidAPI-Host': "noteret-video-no-watermark2.p.rapidapi.com",
            'X-RapidAPI-Key': self.key_api}
        conn.request("GET",
                     "/user/posts?unique_id=%40{0}&user_id={1}"
                     "&count=1000&cursor=0".format(unique_id, self.user_id),
                     headers=headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

    def create_csv_video(self):
        li_unique_id = self._get_li_unique_id()
        df = self._create_videos_df(li_unique_id)
        df.to_csv(self.csv_video)

    def download_videos(self):
        mp4_existed = u_file.filepaths(self.repo_videos)
        df = pd.read_csv(self.csv_video)
        print(f'start download_videos [{len(df)}]')
        for i, (x, row) in enumerate(df.iterrows()):
            print(i)
            url = row['play']
            video_id = row['video_id']
            fname = f'{self.repo_videos}{video_id}.mp4'
            if fname in mp4_existed:
                continue
            try:
                u_url.get(url, fname)
                print(f'{i} - succeed')
            except Exception as e:
                print(e)
                print(f'invalid - {url} - {fname}')
        print('end download_videos')

    def zip_videos(self):
        slices = self.to_slices_videos()
        file = open(self.txt_uploaded, 'a')
        for i, li in enumerate(slices):
            path_zip = f'{self.repo_zip}{str(i).zfill(3)}.zip'
            u_zip.files(li, path_zip)
            for f in li:
                file.write(f'{f}\n')
            print(i)
        file.close()

    def _get_video_list(self, unique_id):
        json = self.get_json(unique_id)
        d = None
        try:
            d = u_json.to_dict(json)
        except Exception as e:
            print('invalid json - ' + unique_id)
            return list
        try:
            return d['data']['videos']
        except Exception as e:
            print('invalid - ' + unique_id)
            return list()

    def _video_dict_to_df(self, d):
        keys_complex = {'music_info', 'author'}
        d_complex = dict()
        for k in keys_complex:
            d_sub = d[k]
            for k_sub in d_sub:
                d_complex[k + '_' + k_sub] = d_sub[k_sub]
            del d[k]
        d.update(d_complex)
        data = {k: [v] for k, v in d.items()}
        return pd.DataFrame(data)

    def _video_li_to_df(self, li):
        df = pd.DataFrame()
        for d in li:
            df_i = self._video_dict_to_df(d)
            df = df.append(df_i)
        return df

    def _get_li_unique_id(self):
        li = list()
        file = open(self.txt_unique_id, 'r')
        for row in file.readlines():
            li.append(row.strip())
        file.close()
        return li

    def _create_videos_df(self, li_unique_id):
        df = pd.DataFrame()
        for unique_id in li_unique_id:
            print(unique_id)
            li_videos = self._get_video_list(unique_id)
            df = df.append(self._video_li_to_df(li_videos))
        return df

    def to_slices_videos(self):
        fnames = list()
        set_uploaded = u_file.to_set(self.txt_uploaded)
        df = pd.read_csv(self.csv_video)
        for i, (x, row) in enumerate(df.iterrows()):
            video_id = row['video_id']
            fname = f'{self.repo_videos}{video_id}.mp4'
            if not fname in set_uploaded:
                fnames.append(fname)
        return u_list.to_slices(li=fnames, size=10)
