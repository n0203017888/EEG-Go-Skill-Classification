# game_RT_time — EEG + 反應時間 多模態分類

把**行為指標（反應時間 RT）**加進 EEG 特徵，檢驗多模態是否能提升棋力分類表現。

**結論：RT 只在 EEG 表現弱的腦區帶來增益，對最強的 Parietal 反而輕微有害。**

## Notebook

| 檔案 | 內容 |
|------|------|
| [svm_eeg_rt_multimodal.ipynb](svm_eeg_rt_multimodal.ipynb) | **主要**：EEG-only vs EEG+RT 五腦區對照 |
| [svm_rt_only.ipynb](svm_rt_only.ipynb) | RT-only 基準線（完全不用 EEG） |

## 實驗設定

- EEG 特徵與腦區分組與 [SVM/svm_session_perturbation.ipynb](../SVM/svm_session_perturbation.ipynb) 完全一致
- RT 特徵：每位受試者每個 session 的**平均 RT**，依 EEG 的 subject × session 排列順序對齊
- 只保留三個 session 都有 RT 資料的受試者
- 評估：LOSO 交叉驗證

## 結果

**分腦區對照（session-level LOSO）**

| 腦區 | EEG-only (Acc / F1) | EEG+RT (Acc / F1) | Acc 差異 |
|------|:---:|:---:|:---:|
| Frontal (7ch) | 0.679 / 0.550 | 0.702 / 0.556 | **+0.024** |
| Central (7ch) | 0.649 / 0.493 | 0.720 / 0.577 | **+0.071** |
| **Parietal (9ch)** | **0.756 / 0.635** | 0.744 / 0.607 | **−0.012** |
| Temporal (6ch) | 0.589 / 0.444 | 0.690 / 0.544 | **+0.101** |
| Occipital (3ch) | 0.565 / 0.422 | 0.542 / 0.374 | **−0.024** |

**全通道（32ch）**

| 設定 | Acc | F1 |
|------|:---:|:---:|
| EEG-only | 0.780 | 0.634 |
| EEG + RT | 0.810 | 0.688 |
| 差異 | +0.030 | +0.054 |

**RT-only 基準線**

| N | Accuracy | Macro-F1 |
|:---:|:---:|:---:|
| 174 | 0.534 | 0.471 |

只用平均 RT 就能達到 0.534（隨機基準為 0.333），代表**反應時間本身確實攜帶棋力資訊**——
強者下得比較快。但這遠低於 EEG 的表現。

## 解讀

增益幅度與該腦區的 EEG 表現**呈反向關係**：

- Temporal（EEG 最弱之一，0.589）→ 增益最大 **+0.101**
- Central（0.649）→ 增益次大 **+0.071**
- Parietal（EEG 最強，0.756）→ **不增反減 −0.012**

合理的解釋是：**RT 所攜帶的棋力資訊，Parietal 區的 EEG 特徵已經涵蓋了。**
在資訊已經足夠的腦區額外加入 RT，只是增加了特徵維度與雜訊，反而稀釋了原本的訊號；
而在資訊不足的腦區，RT 補上了缺口。

> 這也間接支持了主線發現——Parietal 區之所以最強，是因為它捕捉到了與認知處理速度相關的核心訊息。

## 資料檔

- [subject_session_mean_RT.csv](subject_session_mean_RT.csv) — 每位受試者各 session 的平均 RT
