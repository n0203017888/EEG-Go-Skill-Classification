# RT1_ms_predict — 反應時間迴歸（負面結果）

用 Parietal 區的 **190 維特徵**（5 頻帶 × 38 時間點）訓練 SVR，預測每個 trial 的反應時間 `RT1_ms`。

**結論：失敗。相關係數顯著，但模型沒有真正的預測力。** 詳見下方「為什麼說是假象」。

## Notebook

| 檔案 | 內容 |
|------|------|
| [rt_regression_preprocess.ipynb](rt_regression_preprocess.ipynb) | 前處理：五個頻帶 CSV → concat 成 190 維特徵矩陣 |
| [rt_eda.ipynb](rt_eda.ipynb) | RT 分布探索、各 subject 個體差異、per-subject IQR 異常值分析 |
| [rt_regression_model.ipynb](rt_regression_model.ipynb) | **主要**：SVR 訓練與評估（跨群預測 + master 內部 LOSO + per-session） |
| [rt_winrate_scatter.ipynb](rt_winrate_scatter.ipynb) | RT 與勝率的關係（純行為指標分析，不涉及 EEG） |

## 實驗設定

- **特徵**：Parietal 區、5 頻帶 × 38 時間點 = 190 維（`T_19_5s` 因全為空值而排除）
- **模型**：`SVR(kernel='rbf', C=10, gamma='scale', epsilon=500)`
- **訓練策略**：以全部 master trials 訓練，amateur 與 prof 作為完全獨立的測試集
- **另做 master 內部 LOSO** 以評估模型在訓練分布內的泛化能力

## 結果

**跨群預測（train on master）**

| 測試集 | N | MAE | RMSE | R² | Pearson r | p |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|
| Amateur | 2,396 | 13,544.6 ms | 17,314.0 ms | **−0.221** | 0.215 | < 0.0001 |
| Prof | 719 | 11,146.2 ms | 14,575.0 ms | **−0.078** | 0.408 | < 0.0001 |

**Master 內部 LOSO**

| N | MAE | RMSE | R² | Pearson r | p |
|:---:|:---:|:---:|:---:|:---:|:---:|
| — | 12,941.4 ms | 16,391.6 ms | **−0.052** | **−0.363** | < 0.0001 |

**分 session 預測**

| Session | Amateur r | Prof r |
|---------|:---:|:---:|
| ss01 | 0.357 | 0.436 |
| ss02 | 0.214 | 0.409 |
| ss03 | 0.190 | 0.296 |

（全部 p < 0.001）

## ⚠️ 為什麼說相關性是假象

單看 `r = 0.41, p < 0.0001` 會誤以為模型有效。但三個證據推翻這個解讀：

**1. R² 全為負（−0.05 至 −0.22）**
負的 R² 代表模型的預測比「不管輸入是什麼，一律回答訓練集平均值」還要差。
一個真的學到東西的模型不可能做到這件事。

**2. 預測值幾乎是常數**
逐 subject 檢視預測平均（見 notebook 的 subject-level 分析表）：

| | 範圍 |
|---|---|
| 實際 RT 平均 | 21,646 – 39,254 ms（跨度約 17.6 秒） |
| **預測 RT 平均** | **22,112 – 22,294 ms（跨度僅 0.18 秒）** |

模型對每個人輸出的預測幾乎一模一樣，完全沒有在區分個體。

**3. Master 內部 LOSO 出現 r = −0.363**
在訓練分布內部，預測與真值呈**負相關**且高度顯著。
如果模型捕捉到的是真實的 RT 相關訊號，符號不可能翻轉。

**那跨群的正相關從哪來？** 來自群體間的整體分布差異——prof 的 RT 分布本來就與 master 不同，
模型輸出的常數落在兩群之間，就會在合併資料上產生虛假的正相關。

> **這是「統計顯著但實質無意義」的教科書級案例。**
> 若只報告 p 值而不看 R² 與預測值分布，會得出完全相反的結論。

## 圖檔

| 圖 | 說明 |
|----|------|
| `rt_distribution.png` | RT 整體分布（histogram + boxplot） |
| `rt_per_subject.png` | 各 subject 的 RT 分布（violin plot），顯示個體差異之大 |
| `svr_rt_scatter.png` | 預測 vs 實際散布圖 — 可直接看到預測值被壓縮成一條水平帶 |
| `svr_rt_per_session.png` | 分 session 的預測 vs 實際 |
| `rt_winrate_all.png` / `rt_winrate_per_group.png` / `rt_winrate_per_session_group.png` | RT 與勝率的關係（行為指標之間） |

## 資料檔

- [clean_trial_keys.csv](clean_trial_keys.csv) — 清理後保留的 trial 索引
- `master_parietal_190d.csv` — 190 維特徵矩陣（**未納入版控**，見 [.gitignore](../.gitignore)）
