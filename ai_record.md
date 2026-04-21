# AI 對話紀錄 — DRL HW2 (Cliff Walking: Q-learning vs. SARSA)

- **日期**：2026-04-21
- **助手**：Claude Opus 4.7 (1M context)，透過 Claude Code CLI（Anthropic）
- **使用者**：an7172799-ship-it（GitHub）
- **專案**：DRL 課程作業 2 — Q-learning vs. SARSA on Cliff Walking
- **GitHub**：<https://github.com/an7172799-ship-it/HW2-Q-learning-and-SARSA->
- **Live demo**：<https://9hhvhevrdrgp4aaxd5rakm.streamlit.app/>

本檔為此次作業與 Claude 協作的完整對話紀錄，依時間順序逐輪記錄使用者訊息與助手回應。

---

## 第 1 輪 — 作業需求描述

### 使用者

附上兩張參考圖：
1. Sutton & Barto 第 2 版 Fig. 6.4：Sarsa vs. Q-learning Cliff Walking 學習曲線（ε=0.1, α=0.5, 50 runs 平均）。
2. Q-learning policy（沿崖最短路徑長 13） vs. SARSA policy（走上方安全路徑長 17）。

說明：

一、作業目的
實作並比較 Q-learning 與 SARSA，分析學習行為、收斂特性、最終策略差異。

二、環境描述
Cliff Walking 格子世界（如 4×12），起點左下、終點右下，底部中間為懸崖，入懸崖懲罰 −100 並回到起點。

三、問題設定
- 狀態：所有網格位置
- 動作：上、下、左、右
- 獎勵：每步 −1；入懸崖 −100 + 回起點；抵達終點結束
- 策略：ε-greedy（如 ε=0.1）
- 學習率 α：如 0.1
- 折扣 γ：如 0.9
- 訓練回合：至少 500

四、作業內容
1. 實作 Q-learning（off-policy）與 SARSA（on-policy），皆維護 Q(s,a)。
2. 相同環境與參數訓練以確保公平。
3. 結果分析：
   - 學習表現：每回合累積獎勵曲線、收斂速度
   - 策略行為：視覺化最終路徑，冒險 vs 保守
   - 穩定性：波動程度、探索影響

五、理論比較：Off-policy vs On-policy；Q-learning 最優但風險高；SARSA 安全穩定。

六、結論要求：比較收斂、穩定性、適用情境。

### 助手

依 Sutton & Barto 參考圖的設定實作（α=0.5、γ=1.0、ε=0.1、500 episodes × 50 runs）。建立：

- `cliff_walking.py`：4×12 環境，動作空間，獎勵邏輯，`epsilon_greedy` 輔助函式。
- `agents.py`：`run_sarsa`、`run_qlearning`、`average_runs`、`greedy_policy`。
- `main.py`：訓練驅動、繪圖、輸出 `learning_curves.png`、`stability.png`、`policies.png`、`metrics.txt`。

執行 `python main.py`，得到與教科書一致的結果：

| 指標 | SARSA | Q-learning |
| --- | --- | --- |
| 最後 100 回合平均獎勵 | **−26.42** | −49.22 |
| 全程平均獎勵 | **−35.72** | −55.78 |
| 跨 run 每回合標準差 | **31.80** | 69.73 |
| 貪婪路徑長度 | 17（安全） | **13**（最優） |

另撰寫 `README.md` 完整報告（中文），含環境、參數、更新式、結果、討論、結論、參考。

---

## 第 2 輪 — 交付要求：GitHub + ai_record.md + OpenSpec

### 使用者

> 你好 這是一個來自 DRL 課程的作業 2。我想要根據 requirement 來完成這份作業，附圖兩個是參考圖，並且希望會使用到 OpenSpec（附圖）。
>
> 交付文件如下：
> 1. 專案成果（上傳至 GitHub；commit 不能有 Claude co-author）
> 2. 與 AI 的對話紀錄（儲存於本地 `ai_record.md`，由我上傳）

### 助手

- 建立 `ai_record.md`（初版）記錄對話。
- `.gitignore` 加入 `ai_record.md` 與 `.claude/`，讓它不會被 commit。
- `git init`（branch `main`）、暫存所有檔案，**尚未 commit**。
- 詢問 OpenSpec 圖片的細節（附圖中只看到 Cliff Walking 兩張參考圖，沒看到 OpenSpec 圖）：請補充 OpenSpec 在本作業中的用途。

---

## 第 3 輪 — GitHub 目的地 + OpenSpec = spec 優先

### 使用者

> 我要你把東西丟到 https://github.com/an7172799-ship-it/HW2-Q-learning-and-SARSA-.git
> 然後 OpenSpec 是先寫 spec → 產生實作

### 助手

嘗試用 `npx @fission-ai/openspec@1.1.1` 初始化 OpenSpec，但環境沒有 Node.js / npm，於是手動建立 OpenSpec 資料夾結構。

---

## 第 4 輪 — OpenSpec 具體要求（附講義投影片）

### 使用者

附上課程投影片「Lecture 9B Openspec 優化 (4/15)」，其中列出：

1. Install Node.js v24.13.x（劃掉，不必）
2. Install antigravity（劃掉）+ openspec v1.1.1
3. 變更編碼規則：新增變更以「01-」為前綴起始
4. Install GitHub
5. 新增 `dev/startup.sh` 與 `dev/ending.sh`
   - `startup.sh`：pull code from GitHub、讀 handover markdown、建議下一步、`openspec init`
   - `ending.sh`：更新 tasks.md、封存完成的 change、寫 handover markdown、push to GitHub

### 助手

照投影片規格，手動建立完整 OpenSpec v1.1.1 風格的目錄：

```
openspec/
├── project.md             # 專案脈絡與 tech stack
├── AGENTS.md              # AI 協作流程說明
├── changes/
│   └── 01-add-cliff-walking-rl-agents/
│       ├── proposal.md
│       ├── tasks.md
│       └── specs/rl-agents/spec.md
└── specs/
    └── rl-agents/spec.md
```

以及 dev 自動化腳本：

- `dev/startup.sh`：`git pull` → 印 HANDOVER → 列出開啟中的 changes → 建議下一步 → 嘗試 `openspec init`（如果有 CLI）
- `dev/ending.sh`：驗證 tasks.md 全部打勾 → 封存 change（標 `ARCHIVED` 檔案 + 合併 delta spec 到 `openspec/specs/`）→ 重寫 `HANDOVER.md`（含下一個 change 編號）→ commit + push

建立 `HANDOVER.md` 交接文件。改 `README.md` 加入 OpenSpec 與 dev 腳本說明。

設定 git 身份為 `an7172799-ship-it <226669935+an7172799-ship-it@users.noreply.github.com>`（noreply email 讓 GitHub 能自動對應頭像），commit 訊息不含 Claude co-author trailer。

嘗試 push → 403：認證帳號 `sembeiiiii` 對 `an7172799-ship-it/HW2-...` 只有 pull 權限。

---

## 第 5 輪 — GitHub 認證切換失敗

### 使用者

```
C:\Users\a0599>gh auth logout
✓ Logged out of github.com account sembeiiiii

C:\Users\a0599>gh auth login              # 以 an7172799-ship-it 登入
accepts 0 arg(s), received 4

C:\HW2>git push -u origin main
remote: Permission to an7172799-ship-it/HW2-Q-learning-and-SARSA-.git denied to sembeiiiii.
fatal: ... error: 403
```

### 助手

兩個問題：

1. **Windows cmd 不懂 `#` 註解**：後面的中文被當 argv 傳入 `gh auth login`，它回 `accepts 0 arg(s), received 4`。
2. Windows Credential Manager 仍快取舊 `sembeiiiii` 認證，即使重新登入 git 也繼續用舊的。

解法：

```cmd
cd C:\HW2
gh auth login
```
互動選：GitHub.com → HTTPS → Y → Login with a web browser → 用 `an7172799-ship-it` 登入。

登入後清舊認證、改走 gh token：

```cmd
git credential-manager erase
protocol=https
host=github.com

gh auth setup-git
gh api user -q .login
git push -u origin main
```

---

## 第 6 輪 — Device code 沒看到

### 使用者

附上 GitHub Device Authorization 頁面截圖。訊息：`app 沒收到`

### 助手

澄清：那個 8 碼 code（`XXXX-XXXX`）不是 app 推播，是在 **cmd 黑色視窗裡** `gh auth login` 執行時印出來的。往上捲 cmd 視窗就看得到：

```
! First copy your one-time code: XXXX-XXXX
Press Enter to open https://github.com/login/device in your browser...
```

把那串貼到網頁 8 格輸入欄按 Continue。

---

## 第 7 輪 — 登入正確

### 使用者

```
C:\HW2>gh api user -q .login
an7172799-ship-it
```

### 助手

執行 `gh auth setup-git`（會覆蓋 git 的 credential helper 指向新 token），再 `git push -u origin main`。

---

## 第 8 輪 — 首次 push 成功

### 使用者

```
C:\HW2>git push -u origin main
...
To https://github.com/an7172799-ship-it/HW2-Q-learning-and-SARSA-.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

### 助手

Commit `b030933` 已推上 `main`，作者 `an7172799-ship-it`、無 Claude trailer。`ai_record.md` 依要求仍在本地（由 `.gitignore` 忽略）。

---

## 第 9 輪 — 新增 Live demo

### 使用者

> 我的 github 要新增 live demo

### 助手

提供三個選項並建議 A：

- **A. Streamlit Cloud**（推薦）：互動調參、即時訓練、免部署成本。需先在 share.streamlit.io 連 repo。
- **B. GitHub Pages**：純靜態網頁版的 README。
- **C. Google Colab badge**：一顆按鈕跳 Colab 跑 `main.py`。

### 使用者

> A. Streamlit Cloud

### 助手

建立 OpenSpec change `02-add-streamlit-live-demo`：

- `proposal.md`、`tasks.md`、`specs/interactive-demo/spec.md`（delta）
- `streamlit_app.py`：sidebar（α, ε, γ, episodes, runs, seed, 演算法選擇）、Train 按鈕、進度條、兩種演算法的學習曲線、策略圖、summary table
- `requirements.txt`：streamlit + numpy + matplotlib
- README 新增 **Live demo** 段落含部署步驟

封存 change 02 到 `openspec/specs/interactive-demo/spec.md`、更新 HANDOVER.md。commit `0240d07` push 成功。

---

## 第 10 輪 — 極端參數下顯示 bug

### 使用者

附上 Streamlit 截圖：α=0.7、γ=0.65、ε=0.32、500 episodes、6 runs。learning curves 區塊空白；summary 顯示 SARSA last-100 mean = −604.37、Greedy path length = 200；Q-learning last-100 mean = −228.00、path length = 13。

> 你這個有 bug 耶 會跑不出來

### 助手

診斷：不是演算法錯，是**顯示**問題：

1. `ax.set_ylim(-100, 0)` 硬綁：當平均獎勵落在 −200 ~ −600 區間，曲線完全被切出視窗，看起來空白。
2. `200` 剛好是 `trace_greedy_path` 的 `max_steps`：SARSA 在這組極端參數下的貪婪策略繞圈永遠到不了 goal，不該顯示誤導的 `200`。

修正（commit `0b69dca`）：

- **y 軸自動延伸**：當 smoothed curves 最低值 < −100，y-min 延伸到 `ymin * 1.05`；上限永遠 = 0。
- **路徑走不到**：`trace_greedy_path` 改回傳 `(path, reached)`。若 `reached=False` 則 summary 顯示 `∞ (did not reach goal in 200 steps)`。
- **moving_average**：clamp 視窗到 `len(x)`，避免 `smooth ≥ episodes` 時 `np.convolve` 回傳空陣列。

並附上為何那組參數學不好的理論說明：γ=0.65 + 12 步路徑 → 0.65^12 ≈ 0.006，agent 覺得未來的 goal reward 幾乎等於 0，就地繞圈最佳；ε=0.32 又太大導致噪音極多。建議回到 α=0.5、γ=1.0、ε=0.1。

---

## 第 11 輪 — README 要直接放可點連結

### 使用者

附上 README「Live demo」段落截圖（含 4 步部署步驟）。

> 這個直接放可以點進去的連結啦! 不要使用者操作耶

### 助手

拿掉部署步驟，換成大按鈕。但需要使用者提供**真的 Streamlit app URL**（`xxxxx.streamlit.app`），請用戶貼過來。

---

## 第 12 輪 — 作業 requirement 對照檢核

### 使用者

貼上 GitHub 網址（`https://github.com/an7172799-ship-it/HW2-Q-learning-and-SARSA-`，**這是 GitHub repo 而不是 Streamlit app**），並重述作業需求（一、演算法實作；二、訓練過程；三、結果分析），問「你有達到嗎？」

### 助手

澄清：貼錯網址，GitHub ≠ Streamlit app。請再到 share.streamlit.io 複製真 URL 貼過來。

同時做完整 requirement 對照表：

| Requirement | 對應產出 | 位置 |
|---|---|---|
| Q-learning（Off-policy） | `run_qlearning()` | `agents.py` |
| SARSA（On-policy） | `run_sarsa()` | `agents.py` |
| 維護 Q(s,a) | `np.zeros((n_states, n_actions))` | `agents.py` |
| 相同環境與參數 | α=0.5, γ=1.0, ε=0.1 兩者共用 | `main.py` |
| ε-greedy 策略 | `epsilon_greedy()` | `cliff_walking.py` |
| 公平比較 | 50 runs × 500 episodes | `main.py` |
| 累積獎勵曲線 | `learning_curves.png` | repo 根 |
| 收斂速度比較 | README §6.1 | `README.md` |
| 視覺化最終路徑 | `policies.png` 含虛線路徑 | repo 根 |
| 冒險 vs 保守分析 | README §6.2 | `README.md` |
| 波動程度 | `stability.png` + std=31.8 vs 69.7 | repo 根 |
| 探索影響 | README §6.4 | `README.md` |

結論：**全部達成**。

---

## 第 13 輪 — HW spec 參數 + 提供 Streamlit URL

### 使用者

再貼一次作業規格（二、環境描述；三、問題設定），強調：

- ε-greedy、ε=0.1
- α=0.1
- γ=0.9
- ≥ 500 episodes

（接著在下一輪補上 Streamlit URL）

> https://9hhvhevrdrgp4aaxd5rakm.streamlit.app/

### 助手

兩件事一起做成 change `03-hw-spec-params-and-demo-link`：

1. **把 main.py 擴成一次跑兩組參數**：
   - `[sutton]` α=0.5, γ=1.0, ε=0.1（原本）
   - `[hw]` α=0.1, γ=0.9, ε=0.1（新）
   - 輸出 `learning_curves_{hw,sutton}.png`、`stability_{hw,sutton}.png`、`policies_{hw,sutton}.png`、單一 `metrics.txt`（兩組並列）
   - 重構出 `Config` dataclass 和 `run_config()`，迴圈呼叫。

2. **README 裡把 Streamlit URL 做成大按鈕**：

```markdown
## 🚀 [Open Live Demo](https://9hhvhevrdrgp4aaxd5rakm.streamlit.app/)

[![Open in Streamlit](.../streamlit_badge_black_white.svg)](https://9hhvhevrdrgp4aaxd5rakm.streamlit.app/)
```

刪掉原本 1~4 步的部署說明。

重跑訓練 → 新結果：

| 指標 | SARSA (HW) | Q-learning (HW) | SARSA (Sutton) | Q-learning (Sutton) |
| --- | --- | --- | --- | --- |
| last-100 mean | **−23.53** | −49.78 | **−26.42** | −49.22 |
| greedy path length | 17 | **13** | 17 | **13** |

兩組質化結論完全一致。

README 整個 §5–§8 重寫：§5 HW spec（主要）、§6 Sutton（參考）、§7 統一分析、§8 結論。

封存 change 03 到 `openspec/specs/rl-agents/spec.md`（修正 Training driver requirement 為 two-config）、更新 HANDOVER。commit `774b1e4` push 成功。

---

## 第 14 輪 — 本輪：把對話紀錄上 repo

### 使用者

> 我要你把我們兩個詳細的對話紀錄丟掉 github 變成 md 檔案

### 助手

建立 change `04-publish-ai-conversation-log`：

- 從 `.gitignore` 移除 `ai_record.md`
- 重寫 `ai_record.md` 為完整逐字稿（即本檔）
- commit + push

---

## 產出檔案總表（repo 最終狀態）

```
C:\HW2\
├─ cliff_walking.py                     # 4×12 環境
├─ agents.py                            # Q-learning + SARSA
├─ main.py                              # 訓練驅動（兩組 config）
├─ streamlit_app.py                     # Live demo
├─ requirements.txt                     # streamlit, numpy, matplotlib
├─ README.md                            # 中文完整報告（含 live demo 連結）
├─ HANDOVER.md                          # 交接文件（post-03 state）
├─ ai_record.md                         # 本檔
├─ learning_curves_{hw,sutton}.png      # 學習曲線（兩組參數）
├─ stability_{hw,sutton}.png            # 穩定性帶（兩組參數）
├─ policies_{hw,sutton}.png             # 最終策略（兩組參數）
├─ metrics.txt                          # 兩組數值摘要
├─ .gitignore
├─ dev/
│   ├─ startup.sh                       # 開發起始腳本
│   └─ ending.sh                        # 開發收尾腳本
└─ openspec/
   ├─ project.md
   ├─ AGENTS.md
   ├─ changes/
   │  ├─ 01-add-cliff-walking-rl-agents/
   │  │  ├─ ARCHIVED
   │  │  ├─ proposal.md / tasks.md
   │  │  └─ specs/rl-agents/spec.md
   │  ├─ 02-add-streamlit-live-demo/
   │  │  ├─ ARCHIVED
   │  │  ├─ proposal.md / tasks.md
   │  │  └─ specs/interactive-demo/spec.md
   │  ├─ 03-hw-spec-params-and-demo-link/
   │  │  ├─ ARCHIVED
   │  │  ├─ proposal.md / tasks.md
   │  │  └─ specs/rl-agents/spec.md
   │  └─ 04-publish-ai-conversation-log/
   │     ├─ proposal.md / tasks.md
   │     └─ (no spec delta — docs only)
   └─ specs/
      ├─ rl-agents/spec.md              # 當前 source of truth
      └─ interactive-demo/spec.md
```

## Commit 歷史

| Commit | 說明 |
| --- | --- |
| `b030933` | feat: initial implementation of Cliff Walking (Q-learning & SARSA) |
| `0240d07` | feat: add Streamlit live demo (change 02) |
| `0b69dca` | fix(demo): auto y-axis + clearer "did not reach goal" label |
| `774b1e4` | feat: add HW-spec config + embed live-demo URL (change 03) |
| _(pending)_ | docs: publish AI conversation log (change 04) |

所有 commit 作者皆為 `an7172799-ship-it`，無 Claude co-author trailer。
