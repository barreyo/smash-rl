
import logging

from smashrl.train import _main as run_training
from tools.scraper.scrape import _main as download_training_data

log = logging.getLogger(__name__)


def _main():
    log.info("Downloading training data...")
    download_training_data('./data')

    log.info("Running training...")
    run_training('./data')


if __name__ == "__main__":
    log.info("Starting")
    _main()
