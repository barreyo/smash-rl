# Smash RL
Framework to build Reinforcement Learning (RL) AI agents for different
variations of the Super Smash games by Nintendo. The games run on different
platforms, thus several different platforms are supported. Furthermore, the
framework heavily uses [Slippi](https://github.com/project-slippi) which allows
for 'offline' training of agents using replays from tournaments that have been
played in the past.

A couple of pre-tuned RL algorithms are provided in the `algorithms` package.
But it should be fairly easy to bring-your-own snowflake implementation of a RL
agent to play. Pointer on how to do that please see the `smashrl` package.

Current `platform+game` combinations supported:
* `Dolphin Emulator` + `Super Smash Bros Brawl`

## Goals

**Future platforms:**
* Nintendo Switch
* Faster Melee

**Future games:**
* Super Smash Bros Melee
* Super Smash Bros Ultimate (switch)

**Additional future features:**
* Twitch play
* Multi-agent support
* Swappable algorithms (+ more algorithm implementations)

# Installation and Running

**Requirements**:
* Python3.6+

To install all required dependencies into your environment you can run:
```bash
$ make dep-install
```

Steps to generate training data:
TBD

Run an emulator with bot:
TBD

Rest of this section is TBD :neckbeard:

## pip-tools
Dependencies are handled using `pip-tools`, which means they are listed without
version numbers in the `requirements.in` file. This file is then 'compiled' which
collects and pins all required packages in a `requirements.txt` file.

First we need to get `pip-tools`, to install it run:
```bash
$ python3.6 -m pip install -r requirements-dev.txt
```
This command will in addition to installing `pip-tools` install a couple of
handy tools and linters for Python. Please use them :bowtie:

Then we can run `pip-tools` to generate `requirements.txt`:
```bash
$ pip-compile requirements.in
```

To upgrade all dependencies run:
```bash
$ make dep-update
```

# Status
It plays! :fireworks: :beer:

**TODO**:

* Figure out why running off the side, negative rewards wrong? Figure this shit
  out
* Investigate menu states, read from Dolphin memory directly
  * Recover from menu issues, game failures, bot wonkiness
* Train new agent with loooots of data
  * Work out a good reward function
  * Do proper Batching
* Test our DQN against known good environment - OpenAI (FrozenLake, HillRide etc)
* Minimize action space - lots of redudant, useless actions doing the same thing
* Configure headless environment - run in Docker
* Plot reward over time and other stats (avg, sum, etc)
* Train against highest level default bot online
* Add device config object to pass into each device class

# Tests
```bash
$ make tests
```

# Contributing
TBD

# Authors
* [Johan Backman](https://github.com/barreyo)
* [Konstantinos Vaggelakos](https://github.com/kvaggelakos)

# License
TBD
