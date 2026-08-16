# ML_PLV_BE — 多分類器比較與顯著性檢定

固定特徵與流程（PLV + BE、五腦區、PCA 95%、LOSO），只替換分類器，比較 **11 種傳統機器學習模型**，
並用統計檢定驗證「SVM 比較強」這件事是否站得住腳。

## Notebook

| 檔案 | 內容 |
|------|------|
| [ml_plv_be_compare.ipynb](ml_plv_be_compare.ipynb) | 11 分類器 × 5 腦區 完整比較，含 session / hard vote / soft vote 三層評估 |
| [pvalue_analysis.ipynb](pvalue_analysis.ipynb) | McNemar + Wilcoxon 檢定，Holm 多重比較校正 |

## 結果（Parietal 區）

| 分類器 | Session Acc | Hard Vote | Soft Vote | vs SVM |
|--------|:---:|:---:|:---:|:---:|
| **SVM-RBF** | **0.839** | **0.929** | **0.946** | — |
| ExtraTrees | 0.810 | 0.857 | 0.929 | 不顯著 |
| KNN-5 | 0.762 | 0.893 | 0.929 | 不顯著 |
| RandomForest | 0.738 | 0.804 | 0.786 | 部分顯著 |
| LightGBM | 0.732 | 0.839 | 0.875 | 顯著 |
| GradBoost | 0.720 | 0.750 | 0.821 | 部分顯著 |
| XGBoost | 0.702 | 0.768 | 0.768 | 顯著 |
| GaussianNB | 0.631 | 0.696 | 0.696 | 顯著 |
| LogReg | 0.583 | 0.768 | 0.732 | 顯著 |
| LDA | 0.577 | 0.643 | 0.679 | 顯著 |
| MLP | 0.500 | 0.500 | 0.536 | 顯著 |

## 顯著性判定（α = 0.05，Holm 校正後）

| 判定 | 模型 | 說明 |
|------|------|------|
| **不顯著** | ExtraTrees、KNN-5 | 兩種檢定皆未達標（ExtraTrees McNemar p = 0.383、KNN-5 p = 0.052） |
| **部分顯著** | RandomForest、GradBoost | McNemar 達標，但 Wilcoxon 未達標（皆 p = 0.058） |
| **顯著** | 其餘六種 | 兩種檢定皆達標 |

**結論**：SVM-RBF 在數值上領先，但**相對 ExtraTrees 與 KNN-5 的優勢在統計上並不成立**。
把這三者視為同一梯隊、SVM 為其中表現最穩定者，是比較誠實的說法。

> ⚠️ 樣本數限制：投票層級只有 56 位受試者，檢定力有限，不顯著不等於沒有差異。

## 檔案

- [ml_plv_be_accuracy.csv](ml_plv_be_accuracy.csv) / [ml_plv_be_f1.csv](ml_plv_be_f1.csv) — 11 分類器 × 5 腦區的完整數值
- [ml_plv_be_vote.csv](ml_plv_be_vote.csv) — 三層評估（session / hard / soft）逐項數值
- [ml_plv_be_pvalues_vs_svm.csv](ml_plv_be_pvalues_vs_svm.csv) — 各模型 vs SVM 的原始與校正後 p 值
- `ml_plv_be_bar.png` — Acc / F1 長條圖總覽
- `ml_plv_be_heatmap.png` — 分類器 × 腦區熱圖
- `ml_plv_be_top3_cm.png` — 前三名模型的混淆矩陣
