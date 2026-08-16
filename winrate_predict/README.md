# winrate_predict — 勝率迴歸（負面結果）

用 Parietal 區的 **190 維特徵**（5 頻帶 × 38 時間點）訓練 SVR，預測每個 trial 的勝率 `Rate`。

**結論：完全失敗，且是最乾淨的失敗——沒有任何可偵測的訊號。**

## Notebook

| 檔案 | 內容 |
|------|------|
| [winrate_eda_preprocess.ipynb](winrate_eda_preprocess.ipynb) | Rate 分布探索、確認 Rate 是 trial-level 還是 subject-level、建立 190 維特徵矩陣 |
| [winrate_regression_model.ipynb](winrate_regression_model.ipynb) | **主要**：分 session 的 SVR 訓練與評估 |

## 實驗設定

- **特徵**：Parietal 區、5 頻帶 × 38 時間點 = 190 維
- **模型**：`SVR(kernel='rbf', C=10, gamma='scale', epsilon=1.0)`
- **訓練策略**：以 master trials 訓練，amateur 與 prof 作為獨立測試集，分 session 各跑一次

## 結果

| Session | Group | N | Pearson r | p | Spearman r | RMSE |
|---------|-------|:---:|:---:|:---:|:---:|:---:|
| ss01 | amateur | 773 | 0.0534 | 0.138 | 0.0477 | 14.57% |
| ss01 | prof | 240 | 0.0380 | 0.558 | 0.0382 | 13.01% |
| ss02 | amateur | 796 | 0.0164 | 0.644 | 0.0174 | 22.09% |
| ss02 | prof | 239 | −0.0012 | 0.985 | 0.0168 | 20.04% |
| ss03 | amateur | 771 | 0.0081 | 0.822 | 0.0050 | 35.22% |
| ss03 | prof | 240 | 0.0788 | 0.224 | 0.0883 | 29.53% |

**全部六組的 p 值都遠大於 0.05**（最小 p = 0.138），相關係數全部落在 −0.001 ~ 0.079 之間。
這是名副其實的「無訊號」——不像 [RT1_ms_predict/](../RT1_ms_predict/) 那樣還有虛假的顯著相關需要解釋。

## 觀察

**RMSE 隨 session 遞增**（14.6% → 22.1% → 35.2%）。
這反映的是勝率本身的性質：對局越接近終盤，勝率的變動幅度越大
（ss01 的 Rate 範圍 7.5–77.0，ss03 已擴大到 0.2–99.4），
預測難度自然上升，而非模型在後期特別失效——因為它在任何 session 都沒有預測力。

## 圖檔

| 圖 | 說明 |
|----|------|
| `rate_distribution.png` | Rate 的整體分布 |
| `svr_rate_scatter.png` | 預測 vs 實際散布圖 |
| `svr_rate_per_session.png` | 分 session 的預測 vs 實際 |

## 資料檔

`amateur_parietal_190d.csv`、`master_parietal_190d.csv`、`prof_parietal_190d.csv`
— 190 維特徵矩陣（**未納入版控**，見 [.gitignore](../.gitignore)）
