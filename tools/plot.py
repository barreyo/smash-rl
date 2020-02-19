
import logging

import matplotlib.pyplot as plt
import pandas as pd
from watchgod import AllWatcher, run_process

log = logging.getLogger(__name__)


def _main():
    watcher = AllWatcher('/Users/johan/Dev/smash-rl')
    run_process(path='stats.json', target=plot_stuff, watcher_cls=watcher)


def plot_stuff():
    df = pd.read_json('stats.json')
    log.info(df)
    plt.close()
    plt.plot(df)
    plt.show()


if __name__ == "__main__":
    _main()
