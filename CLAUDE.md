# CLAUDE.md — AI 協作守則（gma2-mcp）

給在本 repo 工作的 AI 代理。這些是專案的開發流程規則，請遵守。

## 1. 實作前先「訪談我」（不要猜意圖）

碰到非瑣碎的功能或改動時，**動手寫 code 之前**：

- 假設你還不完全懂我要什麼，**一次問一個問題**，問到清楚為止。
- 釐清四件事：**Goal（目標）/ Input（輸入）/ Output（輸出）/ Steps（步驟與邊界、edge cases）**。
- 把結論寫成一份簡短規格（可存成 `proposal.md` 或寫在對話裡）**給我確認**。
- **我同意前，不要開始寫實作**。寧可多問一題，不要事後返工。

> 瑣碎修改（typo、一行 fix、明確的小調整）可略過訪談，直接做。

## 2. 「完成」的定義 = `make check` 全綠

任何程式碼改動，**做完的標準是 `make check` 全部通過**：

- `make lint` — ruff 檢查 + 格式（可用 `make fix` 自動修）
- `make type` — mypy 型別檢查
- `make test` — pytest（目前 1212 測）

**沒有全綠就不算做完。** 改了 code 一定要補/更新對應測試。

## 3. context 衛生（保持對話短、避免失真壓縮）

- 長對話分階段：每階段把狀態寫進檔案（規格 / `progress.md`），然後用 **`/clear`** 清掉 context、讀回檔案接力——**不必開新 session/重連遠端**，`/clear` 就在當前 session 內清空。
- 大任務拆成獨立模組，**每模組派一個 sub-agent**（短 context），主代理當「監工」讀 `progress.md` 追進度。
- 模組要切乾淨、介面明確，子代理才能各做各的不互相干擾。

## 4. 既有架構慣例

- 分層：`src/commands/`（純函式產生命令字串、不碰網路）→ `src/gma2_client.py`（工作流組合）→ `src/server.py`（MCP 工具）→ `src/telnet_client.py`（連線）。
- grandMA2 定址會用**小數 cue（1.5）與 page.exec 字串**——命令產生器的型別已放寬為 `int | float` / `int | str`，別改回純 int。
- 機密（GMA 帳密等）走 `.env`，**永不進 git**。
