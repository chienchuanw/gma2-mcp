-include .env
export

GMA_HOST ?= 127.0.0.1

.PHONY: server log test lint type check fix

server:
	./connect.sh

log:
	telnet $(GMA_HOST) 30001

test:
	uv run pytest -v

lint:
	uv run ruff check .
	uv run ruff format --check .

type:
	uv run mypy

# 「完成」的定義：lint + 型別 + 測試全綠才算做完
check: lint type test

# 自動修可修的（格式化＋可自動修的 lint）
fix:
	uv run ruff format .
	uv run ruff check --fix .