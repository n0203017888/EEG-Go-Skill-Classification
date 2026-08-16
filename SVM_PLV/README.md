# SVM_PLV — 主要成果 ⭐

本專案最好的結果都在這裡：**PLV + BE 合併特徵、Parietal 腦區、SVM-RBF、三 session 軟投票 → Acc 0.946 / F1 0.943**。

## Notebook

| 檔案 | 內容 |
|------|------|
| **[svm_plv_be_combined.ipynb](svm_plv_be_combined.ipynb)** | ⭐ **主結果**：PLV + BE 合併，五腦區 LOSO，session / hard vote / soft vote 三層評估 |
| [svm_plv_be_combined_visualization.ipynb](svm_plv_be_combined_visualization.ipynb) | 同上流程，額外加入完整的視覺化過程（t-SNE / LDA / KPCA / ternary plot） |
| [svm_plv.ipynb](svm_plv.ipynb) | **只用 PLV** 的基準線，用來對照合併特徵帶來多少增益 |
| [svm_band_ablation.ipynb](svm_band_ablation.ipynb) | 頻帶消融：LOBO（逐一移除）+ 窮舉全部 31 種頻帶子集 |

## 關鍵結果

**腦區比較**（PLV + BE 合併，session-level LOSO）

| 腦區 | Frontal | Central | **Parietal** | Temporal | Occipital |
|------|:---:|:---:|:---:|:---:|:---:|
| Acc | 0.708 | 0.744 | **0.839** | 0.619 | 0.536 |
| F1 | 0.672 | 0.755 | **0.838** | 0.584 | 0.530 |

**特徵互補性**（Parietal）

| 特徵 | Acc |
|------|:---:|
| 只用 PLV | 0.738 |
| 只用 BE | 0.708 |
| **PLV + BE 合併** | **0.839** |

**投票增益**（Parietal，PLV + BE）

| 層級 | N | Acc | F1 |
|------|:---:|:---:|:---:|
| Session-level | 168 | 0.839 | 0.838 |
| Hard Vote | 56 | 0.929 | 0.929 |
| **Soft Vote** | 56 | **0.946** | **0.943** |

**頻帶消融** — 最佳子集 `{delta, alpha, beta}` → **0.863**，優於使用全部五個頻帶（0.839）。
beta 出現在 top-10 子集的全部 10 個、delta 出現 8 個；gamma 貢獻最小（移除後反而上升到 0.863）。

## 圖檔

| 圖 | 說明 |
|----|------|
| `svm_parietal_majority_vote.png` | ⭐ Session vs Hard Vote vs Soft Vote 三張混淆矩陣 |
| `svm_plv_be_combined_confusion.png` | 五腦區混淆矩陣並排 |
| `svm_plv_be_combined_bar.png` | 五腦區 Acc / F1 長條圖 |
| `svm_band_subsets.png` | 31 種頻帶子集搜尋結果 |
| `svm_band_lobo_single.png` | LOBO 與單頻帶表現 |
| `svm_band_ablation_ternary.png` / `_tsne.png` | 頻帶消融的 ternary 與 t-SNE 視覺化 |
| `shap_per_class_top15.png` | SHAP 各類別 top-15 重要特徵 |
| `shap_plv_heatmap.png` / `shap_be_heatmap.png` | SHAP 重要度在 PLV / BE 上的分布 |
| `svm_parietal_tsne.png` / `_lda.png` / `_kpca.png` | 三種降維視覺化，檢視三類的可分性 |
| `svm_parietal_tsne_per_session.png` | 分 session 的 t-SNE |
| `svm_plv_perturbation_box.png` / `_heatmap.png` | session 擾動穩健性 |
| `svm_plv_vs_be_rv.png` | PLV 與 BE 兩組特徵空間的 RV 係數比較 |
| `svm_plv_region5_confusion.png` / `svm_plv_band_importance.png` / `svm_plv_subsets.png` | 只用 PLV 的對應結果 |

## 結果檔

- [svm_plv_results.json](svm_plv_results.json) — 只用 PLV 的五腦區 Acc / F1
- [svm_band_ablation_results.json](svm_band_ablation_results.json) — 完整頻帶消融數值
- `shap_values_best_config.npz` — 最佳配置下的 SHAP values（供重繪用）
