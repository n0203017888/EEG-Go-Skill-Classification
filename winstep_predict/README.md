# winstep_predict — 勝步迴歸（負面結果）

用 Parietal 區的 **190 維特徵**（5 頻帶 × 38 時間點）訓練 SVR，預測每個 trial 的勝步 `Step`。

**結論：完全失敗，與 [winrate_predict/](../winrate_predict/) 同樣沒有任何可偵測的訊號。**

## Notebook

| 檔案 | 內容 |
|------|------|
| [winstep_eda_preprocess.ipynb](winstep_eda_preprocess.ipynb) | Step 分布探索、建立 190 維特徵矩陣 |
| [winstep_regression_model.ipynb](winstep_regression_model.ipynb) | **主要**：分 session 的 SVR 訓練與評估 |

## 實驗設定

- **特徵**：Parietal 區、5 頻帶 × 38 時間點 = 190 維
- **訓練策略**：以 master trials 訓練，amateur 與 prof 作為獨立測試集，分 session 各跑一次

## 結果

| Session | Group | N | Pearson r | p | Spearman r | RMSE |
|---------|-------|:---:|:---:|:---:|:---:|:---:|
| ss01 | amateur | 773 | 0.0120 | 0.740 | 0.0248 | 1.738 |
| ss01 | prof | 240 | 0.0589 | 0.363 | 0.0324 | 1.444 |
| ss02 | amateur | 796 | 0.0170 | 0.633 | 0.0173 | 4.687 |
| ss02 | prof | 239 | 0.0481 | 0.460 | 0.0761 | 2.882 |
| ss03 | amateur | 771 | −0.0353 | 0.328 | −0.0057 | 9.170 |
| ss03 | prof | 240 | −0.0744 | 0.251 | 0.0210 | 10.984 |

**全部六組的 p 值都遠大於 0.05**（最小 p = 0.251），相關係數落在 −0.074 ~ 0.059 之間，
且 ss03 兩組的 Pearson r 已轉為負值——完全符合隨機波動的樣態。

## 觀察

**Step 的值域隨 session 劇烈擴張**：ss01 為 −7.1 ~ 3.0、ss02 為 −7.3 ~ 8.3、ss03 已達 −20.3 ~ 59.2。
RMSE 對應地從 1.7 膨脹到 9.2–11.0。

ss03 的極端值域（最大 59.2）顯示終盤階段的勝步變化極不穩定，
這使得該 session 即使有訊號也極難建模——但由於前兩個 session 在值域穩定時同樣沒有預測力，
無法把失敗歸因於目標變數的難度。

## 圖檔

| 圖 | 說明 |
|----|------|
| `step_distribution.png` | Step 的整體分布 |
| `svr_step_overall.png` | 預測 vs 實際散布圖 |
| `svr_step_per_session.png` | 分 session 的預測 vs 實際 |

## 資料檔

`amateur_parietal_190d.csv`、`master_parietal_190d.csv`、`prof_parietal_190d.csv`
— 190 維特徵矩陣（**未納入版控**，見 [.gitignore](../.gitignore)）
