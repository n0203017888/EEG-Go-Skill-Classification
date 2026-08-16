# SVM — 頻帶能量（BE）分類與穩健性測試

只用**頻帶能量（Band Energy）**特徵的分類實驗，以及各種分類設定與穩健性檢驗。
這裡是專案最早的基準線，後續 [SVM_PLV/](../SVM_PLV/) 才加入 PLV 特徵並取得更好的結果。

📄 方法細節見 **[流程介紹.md](流程介紹.md)**（分腦區流程、LOSO 設計、PCA 原理）

## Notebook

| 檔案 | 內容 |
|------|------|
| [svm_band_energy.ipynb](svm_band_energy.ipynb) | **主要**：只用 BE 的三類分類，五腦區 LOSO |
| [svm_session_perturbation.ipynb](svm_session_perturbation.ipynb) | 穩健性測試：對單一 session 隨機打亂受試者身分，看準確率掉多少 |
| [svm_per_session.ipynb](svm_per_session.ipynb) | 分 session 各自訓練與評估 |
| [data_alignment.ipynb](data_alignment.ipynb) | 資料對齊檢查（subject / session 排列一致性） |
| [svm_amateur_master.ipynb](svm_amateur_master.ipynb) | 二分類：amateur ↔ master |
| [svm_amateur_prof.ipynb](svm_amateur_prof.ipynb) | 二分類：amateur ↔ prof |
| [svm_master_prof.ipynb](svm_master_prof.ipynb) | 二分類：master ↔ prof |
| [_check_misclassified.py](_check_misclassified.py) | 輔助腳本：檢查被分錯的受試者 |

## 只用 BE 的結果（三類，session-level LOSO）

| 腦區 | Frontal | Central | **Parietal** | Temporal | Occipital |
|------|:---:|:---:|:---:|:---:|:---:|
| Acc | 0.643 | 0.601 | **0.708** | 0.577 | 0.500 |
| F1 | 0.615 | 0.575 | **0.691** | 0.555 | 0.492 |

→ 完整數值見 [svm_band_energy_results.json](svm_band_energy_results.json)

Parietal 依然最佳，但只有 0.708；加入 PLV 後合併特徵可達 **0.839**（見 [SVM_PLV/](../SVM_PLV/)）。

## Session 擾動測試

設計：只把**某一個 session** 的 56 位受試者特徵向量隨機重排（讓該 session 的腦電資料錯配到別人的標籤），
另外兩個 session 維持原樣，重跑完整 LOSO。每個「腦區 × session」組合重複 30 次取平均。

用途是驗證**每個 session 是否都實際攜帶了個人身分資訊**——若打亂某 session 後準確率明顯下降，
代表該 session 確實有貢獻，而非三個 session 只是重複同一份資訊。

→ `svm_session_perturbation_region5_bar.png`、`svm_session_perturbation_region5_heatmap.png`

## 圖檔

| 圖 | 說明 |
|----|------|
| `svm_band_energy_band_importance.png` | 各頻帶對分類的重要度 |
| `svm_band_energy_subsets.png` | 頻帶子集搜尋（BE 版本） |
| `svm_region4_loso_confusion.png` | 分腦區 LOSO 混淆矩陣 |
| `svm_region4_per_class.png` | 各類別的 per-class 表現 |
| `svm_session_perturbation_region5_bar.png` / `_heatmap.png` | session 擾動結果 |
