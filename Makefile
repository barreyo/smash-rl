
PROJECT_NAME 		?= smash-rl
TESTS_DIR 			?= tests/
REQUIREMENTS_IN 	?= requirements.in
REQUIREMENTS_TXT 	?= requirements.txt

# Formatting variables
BOLD 			:= $(shell tput bold)
RESET 			:= $(shell tput sgr0)

.PHONY: tests dep-update dep-install clean help

tests:  ## Run all tests using PyTest
	@python3.6 -m pytest -vx -s $(TESTS_DIR)

dep-update:  ## Update all dependencies
	@pip-compile $(REQUIREMENTS_IN) --upgrade

dep-install:  ## Install all python dependencies into environment
	@python3.6 -m pip install -r $(REQUIREMENTS_TXT)

clean:  ## Clean all Python artifacts and dependencies
	@echo "$(BOLD)Remove dependencies...$(RESET)"
	rm -rf src/
	@echo "$(BOLD)Cleaning up Python artifacts and cache files...$(RESET)"
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf .pytest_cache .hypothesis

help:  ## Print this make target help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage: make \033[36m<target>\033[0m\n\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
