#!/bin/bash

DATA_DIR=data/

if [ ! -d "${DATA_DIR}" ]; then
    python3 -m tools.scraper.scrape
fi

if [ -n "$(find "${DATA_DIR}" -maxdepth 0 -type d -empty 2>/dev/null)" ]; then
    python3 -m tools.scraper.scrape
fi

python3 -m smashrl.train ${DATA_DIR}
