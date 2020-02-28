.DEFAULT_GOAL := help
NAMESPACE := courses
NAME := statistical-rethinking

help: ## Show this help
	@echo "${NAMESPACE}-${NAME}"
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | \
	fgrep -v fgrep | sed -e 's/## */##/' | column -t -s##

notebook: ## Start a notebook server
	@jupyter notebook
