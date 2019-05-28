
PROJECT_NAME 	?= smash-rl

# Formatting variables
BOLD 			:= $(shell tput bold)
RESET 			:= $(shell tput sgr0)

.PHONY: dep-update dep-install clean help

dep-update:  ## Update all dependencies
	@pip-compile requirements.in --upgrade

dep-install:  ## Install all python dependencies into environment
	@python3.6 -m pip install -r requirements.txt

clean:  ## Clean all Python artifacts and dependencies
	@echo "$(BOLD)Remove dependencies...$(RESET)"
	rm -rf src/
	@echo "$(BOLD)Cleanup Python artifacts...$(RESET)"
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf .pytest_cache .hypothesis

help:  ## Print this make target help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage: make \033[36m<target>\033[0m\n\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
