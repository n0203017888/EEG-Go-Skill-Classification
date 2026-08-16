"""SVM 3-Class LOSO: 列出所有被分錯的受試者及其預測結果"""
import os, numpy as np, h5py
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from collections import Counter

# ── 資料載入 ──
def get_subject_id(f): return f.split('_ses-')[0]
def scan(folder):
    r = {}
    for f in sorted(os.listdir(folder)):
        if f.endswith('.mat'): r[get_subject_id(f)] = os.path.join(folder, f)
    return r
def load_be(fp):
    with h5py.File(fp,'r') as f: return np.array(f['band_energy']).T

BASE = {'amateur': r'D:\Tseng\圍棋\amateur\band_energy_batch_outputs_2026',
        'master':  r'D:\Tseng\圍棋\master\band_energy_batch_outputs_2026',
        'prof':    r'D:\Tseng\圍棋\prof\band_energy_batch_outputs_2026'}

CLASS_NAMES = ['amateur','master','prof']
maps, complete, raw = {}, {}, {}
for g in CLASS_NAMES:
    ms = {s: scan(os.path.join(BASE[g], s)) for s in ['ss01','ss02','ss03']}
    maps[g] = ms
    complete[g] = sorted(set(ms['ss01']) & set(ms['ss02']) & set(ms['ss03']))
    Xs = []
    for s in ['ss01','ss02','ss03']:
        Xs.append(np.array([load_be(ms[s][sub]) for sub in complete[g]]))
    raw[g] = Xs
    print(f"[{g}] {len(complete[g])} subjects")

# ── 特徵 (top10ch) ──
ch_sel = [0,6,7,10,13,14,21,22,28,31]
def extract(X):
    X = np.log(X+1e-8)[:, :, 1:-1, :].mean(axis=2)
    return X[:, ch_sel, :].reshape(len(X), -1)

subject_ids = complete['amateur'] + complete['master'] + complete['prof']
n_a, n_m, n_p = len(complete['amateur']), len(complete['master']), len(complete['prof'])

feats = []
for g in CLASS_NAMES:
    for X in raw[g]:
        feats.append(extract(X))
X_all = np.vstack(feats)
y_all = np.concatenate([np.zeros(n_a*3), np.ones(n_m*3), np.full(n_p*3, 2)])
subject_split = np.concatenate([np.repeat(complete[g], 3) for g in CLASS_NAMES])
subject_labels = {}
for g_idx, g in enumerate(CLASS_NAMES):
    for s in complete[g]: subject_labels[s] = g_idx

# ── LOSO ──
misclassified = []
for test_sub in subject_ids:
    mask = subject_split == test_sub
    X_tr, y_tr = X_all[~mask], y_all[~mask].astype(int)
    X_te, y_te = X_all[mask],  y_all[mask].astype(int)
    pipe = Pipeline([('sc',StandardScaler()),('pca',PCA(n_components=20)),
                     ('clf',SVC(kernel='rbf',C=10,gamma='scale',class_weight='balanced',random_state=42))])
    pipe.fit(X_tr, y_tr)
    preds = pipe.predict(X_te)
    true_label = subject_labels[test_sub]
    if not (preds == true_label).all():
        misclassified.append({'subject': test_sub, 'true': true_label, 'preds': preds.tolist()})

# ── 顯示 ──
print("\n" + "="*75)
print("SVM 3-Class LOSO (top10ch) — 所有被分錯的受試者")
print("="*75)

for grp_idx, grp_name in enumerate(CLASS_NAMES):
    grp_mis = [m for m in misclassified if m['true'] == grp_idx]
    if not grp_mis: continue
    total_in_grp = {'amateur': n_a, 'master': n_m, 'prof': n_p}[grp_name]
    print(f"\n{'─'*75}")
    print(f"  真實類別: {grp_name.upper()} （{len(grp_mis)}/{total_in_grp} 人有 session 被分錯）")
    print(f"{'─'*75}")
    print(f"  {'Subject':<12s} {'SS01 預測':<14s} {'SS02 預測':<14s} {'SS03 預測':<14s}")
    print(f"  {'-'*54}")
    for m in grp_mis:
        markers = []
        for p in m['preds']:
            name = CLASS_NAMES[p]
            markers.append(f"*{name}*" if p != m['true'] else name)
        print(f"  {m['subject']:<12s} {markers[0]:<14s} {markers[1]:<14s} {markers[2]:<14s}")

n_total = n_a + n_m + n_p
print(f"\n{'='*75}")
print(f"總計有 session 被分錯的人數: {len(misclassified)} / {n_total}")
print(f"全部 session 都正確的人數: {n_total - len(misclassified)} / {n_total}")
print(f"Subject-level Accuracy (全 session 正確): {(n_total - len(misclassified))/n_total:.1%}")
print(f"{'='*75}")

print(f"\n誤分方向統計 (session-level):")
err = Counter()
for m in misclassified:
    tn = CLASS_NAMES[m['true']]
    for p in m['preds']:
        if p != m['true']: err[(tn, CLASS_NAMES[p])] += 1
for (t,p), c in sorted(err.items()):
    print(f"  {t:>8s} -> {p:<8s}: {c} 次")
