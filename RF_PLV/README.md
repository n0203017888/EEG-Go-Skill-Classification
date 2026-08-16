# RF_PLV — Random Forest 版本

與 [SVM_PLV/](../SVM_PLV/) 相同的特徵與流程（PLV + BE、五腦區、LOSO），改用 **Random Forest** 分類器。
主要價值在於 **可解釋性**：樹模型能直接給出 feature importance，也能把單棵決策樹畫出來看。

## Notebook

| 檔案 | 內容 |
|------|------|
| [rf_plv_be_combined.ipynb](rf_plv_be_combined.ipynb) | RF 三類分類、feature importance、單棵樹視覺化、預測信心分析 |
| [add_cells.py](add_cells.py) | 輔助腳本：程式化地對 notebook 增補 cell |

## 結果（PLV + BE，session-level LOSO）

| 腦區 | Frontal | Central | **Parietal** | Temporal | Occipital |
|------|:---:|:---:|:---:|:---:|:---:|
| Acc | 0.637 | 0.643 | **0.738** | 0.577 | 0.577 |
| F1 | 0.505 | 0.525 | **0.715** | 0.481 | 0.534 |

→ 完整數值見 [rf_plv_be_results.json](rf_plv_be_results.json)

RF 在 Parietal 達 0.738，明顯低於 SVM-RBF 的 **0.839**。
在 [ML_PLV_BE/](../ML_PLV_BE/) 的 11 分類器比較中，RandomForest 與 SVM 的差距在 McNemar 檢定下達顯著。

> 注意 F1 與 Acc 的落差（如 Frontal 0.637 vs 0.505）——這是類別不均衡的典型徵兆，
> RF 傾向多預測樣本數最多的 amateur 類，導致 prof 的 recall 偏低。

## 圖檔

| 圖 | 說明 |
|----|------|
| `rf_plv_be_confusion.png` | 五腦區混淆矩陣 |
| `rf_plv_be_bar.png` | 五腦區 Acc / F1 長條圖 |
| `rf_parietal_majority_vote.png` | Parietal 三 session 投票結果 |
| `rf_feature_importance.png` | 特徵重要度排序 |
| `rf_single_tree.png` | 單棵決策樹的完整結構視覺化 |
| `rf_path_confidence.png` | 決策路徑與預測信心分析 |
