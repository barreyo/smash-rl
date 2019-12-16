
import logging
import os
import shutil

import requests

log = logging.getLogger(__name__)

DL_URL = 'https://storage.googleapis.com/slippi.appspot.com{replay_path}'


def download_file(url):
    log.info("Downloading replay: {}".format(url))
    local_filename = os.path.join('./data', url.split('/')[-1])
    r = requests.get(DL_URL.format(replay_path=url), stream=True)
    with open(local_filename, 'wb+') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
