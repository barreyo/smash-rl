
import os
import shutil
import traceback
from multiprocessing import Pool
from pathlib import Path

import requests

BASE_URL = 'https://api-js-dot-slippi.appspot.com/'
DL_URL = 'https://storage.googleapis.com/slippi.appspot.com{replay_path}'
MAX_ATTEMPTS = 3
PER_PAGE = 100

GRAPHQL = """
fragment participantChiclet on Participant {
  _id
  port
  type
  color
  nametag
  character {
    id
    __typename
  }
  __typename
}

fragment matchupDisplay on Game {
  _id
  participants {
    _id
    port
    ...participantChiclet
    __typename
  }
  __typename
}

fragment gameTable on Tournament {
  _id
  games(first: $matchupDisplayFirst, offset: $matchupDisplayOffset) {
    _id
    path
    station
    stage
    startAt
    ...matchupDisplay
    __typename
  }
  __typename
}

query GameTableComponent($id: Int!, $matchupDisplayFirst: Int!, $matchupDisplayOffset: Int!) {
  tournament(_id: $id) {
    ...gameTable
    __typename
  }
}
"""  # noqa

p = Pool(20)


def generate_payload(tournament, first, offset):
    return {
        "operationName": "GameTableComponent",
        "variables": {
            "id": tournament,
            "matchupDisplayFirst": first,
            "matchupDisplayOffset": offset
        },
        "query": GRAPHQL
    }


def get_all_replays(tournament):
    offset = 0
    while True:
        print("Getting page with offset: {}".format(offset))
        more = get_replays(tournament, PER_PAGE, offset)
        offset += PER_PAGE
        if not more:
            break


def get_replays(tournament, first, offset):
    try:
        replays = requests.post(BASE_URL, json=generate_payload(
            tournament, first, offset)).json()
        if len(replays['data']['tournament']['games']) > 0:
            download_replays(replays)
            return True
        else:
            return False
    except Exception as e:
        print("Saw issue: {e}".format(e=e))
        traceback.print_exc()


def download_replays(replays):
    files = list(
        map(lambda g: g['path'], replays['data']['tournament']['games']))
    p.map(download_file, files)


def download_file(url):
    print("Downloading replay: {}".format(url))
    local_filename = os.path.join('./data', url.split('/')[-1])
    r = requests.get(DL_URL.format(replay_path=url), stream=True)
    with open(local_filename, 'wb+') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)


if __name__ == "__main__":
    Path('./data/').mkdir(exist_ok=True, parents=True)
    for t in [3, 40]:  # Tournaments
        get_all_replays(t)
    p.terminate()
    p.join()
