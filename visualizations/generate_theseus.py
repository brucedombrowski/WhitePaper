#!/usr/bin/env python3
"""
Generate git-of-theseus plots for Security Toolkit.
Produces cohort stack plots, survival curves, and extension breakdown.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import numpy as np
from datetime import datetime
from pathlib import Path

try:
    import scienceplots
    plt.style.use(['science', 'ieee', 'no-latex'])
except Exception:
    plt.style.use('seaborn-v0_8-paper')

try:
    import matplot2tikz
    HAS_TIKZ = True
except Exception:
    HAS_TIKZ = False

OUTPUT_DIR = Path(__file__).parent
THESEUS_DIR = OUTPUT_DIR / 'theseus'


def save_figure(fig, name):
    """Save figure as PNG and PDF."""
    png_path = OUTPUT_DIR / f'{name}.png'
    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f'  Saved: {png_path}')

    pdf_path = OUTPUT_DIR / f'{name}.pdf'
    fig.savefig(pdf_path, bbox_inches='tight', facecolor='white')
    print(f'  Saved: {pdf_path}')

    if HAS_TIKZ:
        try:
            tikz_path = OUTPUT_DIR / f'{name}.tex'
            matplot2tikz.save(str(tikz_path))
            print(f'  Saved: {tikz_path}')
        except Exception as e:
            print(f'  TikZ export skipped: {e}')


def load_json(filename):
    with open(THESEUS_DIR / filename) as f:
        return json.load(f)


# ============================================================================
# Helper: parse theseus new-format JSON (keys: y, ts, labels)
# ============================================================================
def parse_theseus_data(data):
    """Parse git-of-theseus v0.3+ JSON format: {y: [[...]], ts: [...], labels: [...]}"""
    ts_strs = data['ts']
    dates = [matplotlib.dates.date2num(datetime.fromisoformat(t)) for t in ts_strs]
    labels = data['labels']
    y = np.array(data['y'])  # shape: (n_labels, n_timestamps)
    return dates, labels, y


# ============================================================================
# Cohort Stack Plot (code age analysis)
# ============================================================================
print('Theseus Chart 1: Code cohort analysis...')
cohorts = load_json('cohorts.json')
dates, labels, y = parse_theseus_data(cohorts)

fig, ax = plt.subplots(figsize=(8, 4))
ax.stackplot(dates, y, labels=labels, alpha=0.85)
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d'))
ax.set_xlabel('Date (2026)')
ax.set_ylabel('Lines of Code')
ax.set_title('Security Toolkit: Code Age Cohorts')
ax.legend(loc='upper left', fontsize=7, title='Written in', title_fontsize=8)
ax.grid(True, alpha=0.3, axis='y')
fig.autofmt_xdate()
save_figure(fig, 'theseus_cohorts')
plt.close()

# ============================================================================
# Survival Plot (Kaplan-Meier style)
# ============================================================================
print('Theseus Chart 2: Code survival curve...')
survival = load_json('survival.json')

fig, ax = plt.subplots(figsize=(8, 4))
# survival.json keys are commit hashes with list values (fraction surviving over time)
# We need to aggregate these into a single mean survival curve
all_curves = []
for key, values in survival.items():
    if isinstance(values, list) and len(values) > 0 and isinstance(values[0], (int, float)):
        all_curves.append(values)

if all_curves:
    # Pad to same length and compute mean
    max_len = max(len(c) for c in all_curves)
    padded = np.full((len(all_curves), max_len), np.nan)
    for i, c in enumerate(all_curves):
        padded[i, :len(c)] = c
    mean_survival = np.nanmean(padded, axis=0)
    days = np.arange(max_len)

    ax.plot(days, mean_survival, color='#1f77b4', linewidth=2, label='Mean survival')
    ax.fill_between(days, mean_survival, alpha=0.2, color='#1f77b4')

    # Add percentile bands if enough data
    if len(all_curves) > 5:
        p25 = np.nanpercentile(padded, 25, axis=0)
        p75 = np.nanpercentile(padded, 75, axis=0)
        ax.fill_between(days, p25, p75, alpha=0.15, color='#1f77b4', label='25th-75th percentile')

ax.set_xlabel('Days Since Written')
ax.set_ylabel('Fraction of Code Surviving')
ax.set_title('Security Toolkit: Code Survival Curve (Kaplan-Meier)')
ax.set_ylim(0, 1.05)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=8)
save_figure(fig, 'theseus_survival')
plt.close()

# ============================================================================
# Extension Stack Plot (language evolution)
# ============================================================================
print('Theseus Chart 3: Language/extension evolution...')
exts = load_json('exts.json')
dates, labels, y = parse_theseus_data(exts)

fig, ax = plt.subplots(figsize=(8, 4))

# Sort by max LOC (largest first for stackplot)
max_vals = y.max(axis=1)
sort_idx = np.argsort(-max_vals)[:8]
y_sorted = y[sort_idx]
labels_sorted = [labels[i] if labels[i] else '(no ext)' for i in sort_idx]

ax.stackplot(dates, y_sorted, labels=labels_sorted, alpha=0.85)
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d'))
ax.set_xlabel('Date (2026)')
ax.set_ylabel('Lines of Code')
ax.set_title('Security Toolkit: Code by File Extension Over Time')
ax.legend(loc='upper left', fontsize=7)
ax.grid(True, alpha=0.3, axis='y')
fig.autofmt_xdate()
save_figure(fig, 'theseus_extensions')
plt.close()

# ============================================================================
# Directory Stack Plot
# ============================================================================
print('Theseus Chart 4: Directory structure evolution...')
dirs = load_json('dirs.json')
dates, labels, y = parse_theseus_data(dirs)

fig, ax = plt.subplots(figsize=(8, 4))

# Sort by max LOC
max_vals = y.max(axis=1)
sort_idx = np.argsort(-max_vals)[:8]
y_sorted = y[sort_idx]
labels_sorted = [labels[i] for i in sort_idx]

ax.stackplot(dates, y_sorted, labels=labels_sorted, alpha=0.85)
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d'))
ax.set_xlabel('Date (2026)')
ax.set_ylabel('Lines of Code')
ax.set_title('Security Toolkit: Code by Directory Over Time')
ax.legend(loc='upper left', fontsize=6, ncol=2)
ax.grid(True, alpha=0.3, axis='y')
fig.autofmt_xdate()
save_figure(fig, 'theseus_directories')
plt.close()

print('\n=== Theseus charts done! ===')
