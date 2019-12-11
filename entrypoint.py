
from smashrl.train import _main as run_training
from tools.scraper.scrape import _main as download_training_data


def _main():
    download_training_data('./data')
    run_training('./data')


if __name__ == "__main__":
    _main()
