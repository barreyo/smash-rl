
import os
import shutil

import requests

DL_URL = 'https://storage.googleapis.com/slippi.appspot.com{replay_path}'


def download_file(url):
    print("Downloading replay: {}".format(url))
    local_filename = os.path.join('./data', url.split('/')[-1])
    r = requests.get(DL_URL.format(replay_path=url), stream=True)
    with open(local_filename, 'wb+') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
