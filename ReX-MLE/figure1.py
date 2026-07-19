from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager


# Optional: place Google Sans font files next to this script.
script_dir = Path(__file__).resolve().parent
font_dir = script_dir / "Google-Sans-Font"

if font_dir.exists():
    for font_path in font_dir.glob("*.ttf"):
        font_manager.fontManager.addfont(str(font_path))
    mpl.rcParams["font.family"] = "Google Sans"
else:
    mpl.rcParams["font.family"] = "DejaVu Sans"

mpl.rcParams["axes.unicode_minus"] = False


# Task-level primary metric values. Column order:
# [AIDE, ML-Master, R&D Agent, AMID, Human Winner]
# FAIL is treated as 0. LDCT-IQA is normalized by dividing its score by 3.
segmentation_tasks = {
    "ISLES'22": [0.04182, 0.00, 0.02, 0.71, 0.79],
    "NeurIPS-CellSeg": [0.04, 0.04, 0.36, 0.90, 0.88],
    "PANTHER-T1": [0.33, 0.13, 0.16, 0.42, 0.73],
    "PANTHER-T2": [0.09, 0.05, 0.28, 0.31, 0.53],
    "PUMA-T1-Seg": [0.00, 0.00, 0.00, 0.56, 0.78],
    "PUMA-T2-Seg": [0.00, 0.00, 0.00, 0.56, 0.78],
    "SEG.A": [0.02, 0.02, 0.00, 0.91, 0.92],
    "TopBrain-CTA": [0.03, 0.26, 0.08, 0.59, 0.79],
    "TopBrain-MRA": [0.01, 0.26, 0.50, 0.64, 0.81],
    "TopCoW-CTA-Seg": [0.09, 0.25, 0.49, 0.63, 0.87],
    "TopCoW-MRA-Seg": [0.11, 0.48, 0.73, 0.76, 0.88],
}

detection_tasks = {
    "DENTEX": [0.09, 0.08, 0.09, 0.49, 0.40],
    "PUMA-T1-Det": [0.02, 0.08, 0.06, 0.54, 0.66],
    "PUMA-T2-Det": [0.00, 0.00, 0.01, 0.28, 0.27],
    "TopCoW-CTA-Det": [0.67, 0.65, 0.70, 0.71, 0.79],
    "TopCoW-MRA-Det": [0.66, 0.69, 0.19, 0.74, 0.85],
}

classification_tasks = {
    "TopCoW-CTA-Cls": [0.33, 0.10, 0.28, 0.33, 0.73],
    "TopCoW-MRA-Cls": [0.33, 0.33, 0.09, 0.46, 0.89],
}

image_quality_tasks = {
    "LDCT-IQA": [2.62482 / 3, 2.50 / 3, 2.66 / 3, 2.74 / 3, 2.74 / 3],
    "USenhance": [0.11, 0.13, 0.00, 0.19, 0.91],
}


def category_average(task_dict: dict[str, list[float]]) -> np.ndarray:
    """Calculate the mean primary metric for each model in a category."""
    values = np.asarray(list(task_dict.values()), dtype=float)
    if values.ndim != 2 or values.shape[1] != 5:
        raise ValueError(
            "Each task must contain [AIDE, ML-Master, R&D Agent, AMID, Human Winner]."
        )
    return values.mean(axis=0)


categories = [
    "Segmentation",
    "Detection",
    "Classification",
    "Image Quality & Enhancement",
]
category_values = np.vstack(
    [
        category_average(segmentation_tasks),
        category_average(detection_tasks),
        category_average(classification_tasks),
        category_average(image_quality_tasks),
    ]
)
model_names = ["AIDE", "ML-Master", "R&D Agent", "AMID", "Human Winner"]

print("Category-average values:")
for category, row in zip(categories, category_values):
    formatted = ", ".join(
        f"{model}: {value:.4f}" for model, value in zip(model_names, row)
    )
    print(f"{category}: {formatted}")


fig, ax = plt.subplots(figsize=(13.5, 5.4))
background_color = "#FEFFFE"
fig.patch.set_facecolor(background_color)
ax.set_facecolor(background_color)

x = np.arange(len(categories))
bar_width = 0.115
offsets = np.array([-2, -1, 0, 1, 2]) * bar_width
colors = {
    "AIDE": "#4B4B4B",
    "ML-Master": "#777777",
    "R&D Agent": "#A1A1A1",
    "AMID": "#377EB8",
    "Human Winner": "#A41034",
}

for model_index, model_name in enumerate(model_names):
    ax.bar(
        x + offsets[model_index],
        category_values[:, model_index],
        width=bar_width,
        color=colors[model_name],
        label=model_name,
        edgecolor="white",
        linewidth=1.3,
        zorder=3,
    )

ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=13)
ax.set_yticks(np.arange(0, 1.01, 0.2))
ax.set_yticklabels(["0", "0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=13)
ax.set_ylim(0, 1.05)
ax.set_ylabel("Average Metric Score", fontsize=17)
ax.set_title("AI Agent Performance on ReX-MLE", fontsize=18, fontweight="medium", pad=8)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(1.5)
ax.spines["bottom"].set_linewidth(1.5)
ax.tick_params(axis="both", width=1.2)
ax.set_axisbelow(True)
ax.xaxis.grid(True, linestyle="-", linewidth=1, alpha=0.25)
ax.yaxis.grid(False)
ax.legend(
    frameon=False,
    fontsize=12.5,
    ncol=5,
    loc="upper center",
    bbox_to_anchor=(0.62, 0.995),
    columnspacing=1.3,
    handlelength=1.7,
)

plt.tight_layout()
output_path = script_dir / "figure1.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close(fig)
print(f"Saved to: {output_path}")
