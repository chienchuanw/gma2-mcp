-include .env
export

GMA_HOST ?= 127.0.0.1

.PHONY: server log test

server:
	./connect.sh

log:
	telnet $(GMA_HOST) 30001

test:
	uv run pytest -v