#!/usr/bin/env bash

# 從 .env 檔案載入環境變數
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# 設定預設值（如果 .env 沒有設定或值為空，則使用預設值）
GMA_HOST="${GMA_HOST:-2.0.0.166}"
GMA_PORT="${GMA_PORT:-30000}"

# 帳號密碼：優先使用 .env 的設定，否則使用預設值
if [ -z "$GMA_USER" ]; then
    GMA_USER="administrator"
fi

if [ -z "$GMA_PASSWORD" ]; then
    GMA_PASSWORD="admin"
fi

echo "Connecting to $GMA_HOST:$GMA_PORT as $GMA_USER..."

# 使用 expect 自動登入後進入互動模式
expect -c "
spawn telnet $GMA_HOST $GMA_PORT
sleep 1
send \"login \\\"$GMA_USER\\\" \\\"$GMA_PASSWORD\\\"\\r\"
interact
"

