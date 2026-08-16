# docs — 專案文件

| 檔案 | 內容 |
|------|------|
| [dataset_info.md](dataset_info.md) | **資料集規格**：受試者列表、trial 數異常紀錄、檔案命名格式、`.set` 檔結構與讀取方式 |
| [專案總覽.md](專案總覽.md) | **完整實驗記錄**：所有測試的方法與結果，比根目錄 README 更詳細 |
| `EEG圍棋棋力分類_成果報告.docx` | 成果報告（Word） |
| `svm分析.docx` | SVM 分析報告（Word） |

## 從哪裡開始讀

1. **[根目錄 README](../README.md)** — 核心成果與圖表，五分鐘看完全貌
2. **[專案總覽.md](專案總覽.md)** — 每個實驗的細節與數字
3. **[dataset_info.md](dataset_info.md)** — 要動手跑之前必讀
4. **[../SVM/流程介紹.md](../SVM/流程介紹.md)** — 分腦區流程、LOSO 設計、PCA 原理

## ⚠️ 已修正的數值

`專案總覽.md` 早期版本有三處與實際結果檔不符，已依據 notebook 輸出與結果 JSON 修正：

| 項目 | 原記載 | 實際 | 依據 |
|------|--------|------|------|
| 只用 BE 的 Parietal Acc | 0.738 | **0.708** | [svm_band_energy_results.json](../SVM/svm_band_energy_results.json) |
| 與 SVM 無顯著差異的模型 | 僅 ExtraTrees | **ExtraTrees + KNN-5** | [ml_plv_be_pvalues_vs_svm.csv](../ML_PLV_BE/ml_plv_be_pvalues_vs_svm.csv) |
| RT 迴歸 | r ≈ 0.01–0.08，不顯著 | **r = 0.19–0.44，p < 0.001，但 R² 為負** | `rt_regression_model.ipynb` 輸出 |

RT 那一項的修正最關鍵：原本被歸類為「與勝率、勝步相同的隨機結果」，
實際上是**顯著但無意義**的相關——結論仍是失敗，但失敗的性質完全不同。
詳見 [../RT1_ms_predict/README.md](../RT1_ms_predict/README.md)。
