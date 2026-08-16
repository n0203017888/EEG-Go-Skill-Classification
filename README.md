# EEG 圍棋棋力分類

> 用傳統機器學習（以 SVM 為主）從 EEG 腦波訊號分類圍棋選手的棋力等級。

以 EEG 的**功能連結（PLV）**與**頻帶能量（BE）**兩種特徵，經腦區分群 → PCA 降維 → SVM-RBF 分類，
區分圍棋棋力三個等級（amateur / master / prof）。
最佳配置為**頂葉（Parietal）區 + 三個 session 軟投票**，達 **Accuracy 0.946 / Macro-F1 0.943**。

---

## 主要結果

**腦區 = Parietal，特徵 = PLV + BE 合併，分類器 = SVM-RBF，LOSO 交叉驗證**

| 評估層級 | N | Accuracy | Macro-F1 |
|----------|----|----------|----------|
| Session-level | 168 | 0.839 | 0.838 |
| Hard Vote（3 session 硬投票） | 56 | 0.929 | 0.929 |
| **Soft Vote（3 session 軟投票）** | 56 | **0.946** | **0.943** |

**六個重點**

1. **最佳配置**：Parietal + PLV+BE + SVM-RBF + 三 session 軟投票 → Acc 0.946
2. **投票是關鍵增益**：session 層級 84% → 投票後 93–95%
3. **PLV 與 BE 互補**，合併明顯優於單用其一；頂葉區資訊量最高
4. **beta / delta 頻帶最重要**，gamma 幫助最小（最佳頻帶子集 `{delta, alpha, beta}` → 0.863）
5. **SVM-RBF 在 11 種傳統模型中最強**，經 McNemar + Wilcoxon（Holm 校正）檢定驗證
6. **分類成功、迴歸失敗** → 特徵反映的是長期棋力，而非即時表現（見下方「負面結果」）

完整分析與其他消融實驗請見 **[docs/專案總覽.md](docs/專案總覽.md)**。

---

## 負面結果（誠實記錄）

嘗試用同一批 EEG 特徵**迴歸預測行為指標**，結果全部接近隨機（r ≈ 0.01–0.08，p > 0.1）：

| 目標 | 資料夾 | 結果 |
|------|--------|------|
| 反應時間 RT（毫秒） | [RT1_ms_predict/](RT1_ms_predict/) | MAE ≈ 11–13 秒，基本無預測力 |
| 勝率 winrate | [winrate_predict/](winrate_predict/) | Pearson r ≈ 0.02–0.08（不顯著） |
| 勝步 winstep | [winstep_predict/](winstep_predict/) | Pearson r ≈ 0.01–0.07（不顯著） |

這批特徵捕捉的是**穩定的個人專業度**，而非**當下的表現波動**。

---

## 資料集

| 項目 | 值 |
|------|------|
| 受試者 | 57 人（amateur 28 / master 21 / prof 8） |
| 總 trials | 5,096 |
| 取樣率 / 通道 | 500 Hz / 36 通道（常用前 32） |
| Trial 長度 | 21 秒（10,500 samples） |
| Session | 3 個（ss01 開局 / ss02 中盤 / ss03 尾盤） |
| 格式 | EEGLAB `.set` + `.fdt` |

**原始 EEG 資料與受試者級特徵檔並未包含在本 repo 中**（人體實驗資料，需另行申請）。
完整規格、檔案命名、讀取方式見 **[docs/dataset_info.md](docs/dataset_info.md)**。

Notebook 預設從本機絕對路徑讀取原始資料（如 `D:\Tseng\圍棋\`），
在其他機器執行需自行調整路徑常數。

---

## 專案結構

| 資料夾 | 內容 |
|--------|------|
| [SVM_PLV/](SVM_PLV/) | ⭐ 主要成果：PLV+BE 合併分類、頻帶消融、SHAP 解釋、t-SNE/LDA/KPCA 視覺化 |
| [SVM/](SVM/) | 只用 BE 的分類、二分類設定、session 擾動測試、[流程介紹](SVM/流程介紹.md) |
| [ML_PLV_BE/](ML_PLV_BE/) | 11 種分類器比較 + 顯著性檢定（McNemar / Wilcoxon） |
| [RF_PLV/](RF_PLV/) | Random Forest 版本（單棵樹視覺化、feature importance） |
| [RT1_ms_predict/](RT1_ms_predict/) | 反應時間迴歸（負面結果） |
| [winrate_predict/](winrate_predict/) | 勝率迴歸（負面結果） |
| [winstep_predict/](winstep_predict/) | 勝步迴歸（負面結果） |
| [game_RT_time/](game_RT_time/) | EEG + RT 多模態分類 |
| [docs/](docs/) | 資料集說明、專案總覽、成果報告（.docx） |

**入口 notebook**：[SVM_PLV/svm_plv_be_combined.ipynb](SVM_PLV/svm_plv_be_combined.ipynb)（最佳結果）

---

## 環境安裝

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
jupyter lab
```

---

## 授權

程式碼採 [MIT License](LICENSE)。EEG 原始資料與衍生特徵資料不在此授權範圍內。
