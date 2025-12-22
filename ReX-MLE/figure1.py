import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager
from pathlib import Path

# ---------------------------------------------------------
# Load Google Sans
# ---------------------------------------------------------
font_dir = Path("/home/xiz569/rajpurkarlab/med-mle-bench/manuscript/figures/Google-Sans-Font")
for font_path in font_dir.glob("*.ttf"):
    font_manager.fontManager.addfont(font_path)
mpl.rcParams["font.family"] = "Google Sans"

# ---------------------------------------------------------
# Task-level values (FAIL = 0)
# Format: [AIDE, ML-Master, R&D Agent, Winner]
# ---------------------------------------------------------

seg_tasks = {
    "ISLES'22":              [0.04182, 0.00, 0.02, 0.79],
    "NeurIPS-CellSeg":       [0.04,    0.04, 0.36, 0.88],
    "PANTHER-T1":            [0.33,    0.13, 0.16, 0.73],
    "PANTHER-T2":            [0.09,    0.05, 0.28, 0.53],
    "PUMA-T1-Seg":           [0.0,     0.00, 0.00, 0.78],
    "PUMA-T2-Seg":           [0.00,    0.00, 0.00, 0.78],
    "SEG.A":                 [0.02,    0.02, 0.00, 0.92],
    "TopBrain-CTA":          [0.03,    0.26, 0.08, 0.79],
    "TopBrain-MRA":          [0.01,    0.26, 0.50, 0.81],
    "TopCoW-CTA-Seg":        [0.09,    0.25, 0.49, 0.87],
    "TopCoW-MRA-Seg":        [0.11,    0.48, 0.73, 0.88],
}


det_tasks = {
    "DENTEX":                [0.09, 0.08, 0.09, 0.40],   # ML-Master = FAIL → 0
    "PUMA-T1-Det":           [0.02, 0.08, 0.06, 0.66],
    "PUMA-T2-Det":           [0.0,  0.00, 0.01, 0.27],
    "TopCoW-CTA-Det":        [0.67, 0.65, 0.70, 0.79],
    "TopCoW-MRA-Det":        [0.66, 0.69, 0.19, 0.85],
}

cls_tasks = {
    "TopCoW-CTA-Cls":        [0.33, 0.10, 0.28, 0.73],
    "TopCoW-MRA-Cls":        [0.33, 0.33, 0.09, 0.89],
}

iqa_tasks = {
    "LDCT-IQA":              [2.62482/3, 2.50/3, 2.66/3, 2.74/3],   # ← normalize /3
    "USenhance":             [0.11, 0.13, 0.0, 0.91],
}

# ---------------------------------------------------------
# Compute averaged metrics per category
# ---------------------------------------------------------
def category_avg(task_dict):
    arr = np.array(list(task_dict.values()))  # (n_tasks, 4)
    return arr.mean(axis=0)                   # returns [AIDE, ML, RD, Winner]

avg_seg = category_avg(seg_tasks)
avg_det = category_avg(det_tasks)
avg_cls = category_avg(cls_tasks)
avg_iqa = category_avg(iqa_tasks)

categories = ["Segmentation", "Detection", "Classification", "Image Quality & Enhancement"]
values = np.vstack([avg_seg, avg_det, avg_cls, avg_iqa])  # shape (4, 4)

AIDE     = values[:, 0]
MLMaster = values[:, 1]
RDAgent  = values[:, 2]
Winner   = values[:, 3]

x = np.arange(len(categories))

# ---------------------------------------------------------
# Plot setup
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 5))
fig.patch.set_facecolor("#FEFFFE")
ax.set_facecolor("#FEFFFE")

# Slightly slimmer bars for more breathing room
bar_width = 0.12
# Grayscale palette for agents (dark → light)
colors = {
    "AIDE": "#4B4B4B", #"#B0B0B0", #"#4B4B4B",
    "ML-Master": "#777777", #"#CCCCCC", #"#777777",
    "R&D Agent": "#A1A1A1", # "#EEEEEE", # "#A1A1A1",
    "Human Winner":  "#a41034" #"#AEC1FE" #"#1E7AD3",
}

# ---------------------------------------------------------
# Draw bars
# ---------------------------------------------------------
ax.bar(x - 1.5 * bar_width, AIDE,     bar_width, color=colors["AIDE"],        label="AIDE",         edgecolor="white", linewidth=1.5)
ax.bar(x - 0.5 * bar_width, MLMaster, bar_width, color=colors["ML-Master"],   label="ML-Master",    edgecolor="white", linewidth=1.5)
ax.bar(x + 0.5 * bar_width, RDAgent,  bar_width, color=colors["R&D Agent"],   label="R&D Agent",    edgecolor="white", linewidth=1.5)
ax.bar(x + 1.5 * bar_width, Winner,   bar_width, color=colors["Human Winner"], label="Human Winner", edgecolor="white", linewidth=1.5)

# ---------------------------------------------------------
# Formatting
# ---------------------------------------------------------
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=14)
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(['0', '0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=14)
ax.set_ylabel("Average Metric Score", fontsize=18)

# right and upper spines to False
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.set_ylim(0, 1.05)

# only x lines no grid
ax.xaxis.grid(True, linestyle="-", alpha=0.3)
# ax.grid(True, linestyle="-", alpha=0.3)

for spine in ax.spines.values():
    spine.set_linewidth(1.5)

plt.title("AI Agent Performance on ReX-MLE (GPT-5)", fontsize=18, fontweight="medium")
plt.legend(frameon=False, fontsize=14, ncol=4)

plt.tight_layout()
plt.savefig("figure1.png", dpi=300)
plt.show()
