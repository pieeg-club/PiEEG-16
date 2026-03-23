"""
PiEEG-16 Spike Removal Script
-------------------------------
Detects and removes spike rows caused by SPI protocol failures between
Raspberry Pi and PiEEG-16. When a spike is detected in ANY channel,
the entire row (all 16 channels) is removed to preserve EEG data alignment.

Detection method: IQR-based outlier detection (robust to non-normal EEG distributions).
A sample is flagged as a spike if it exceeds:  Q3 + N*IQR  or falls below  Q1 - N*IQR
Default multiplier N=10 is conservative — only catches true protocol glitches.
"""

import pandas as pd
import numpy as np
import os
import sys


# ── Configuration ─────────────────────────────────────────────────────────────

INPUT_FILE  = "output4.xlsx"   # ← change if needed
OUTPUT_FILE = "output_cleaned.xlsx"

# IQR multiplier for spike detection.
# 10 = very conservative (only catches extreme glitches).
# Lower values (e.g. 5) catch more marginal spikes.
IQR_MULTIPLIER = 10

# ── Load data ─────────────────────────────────────────────────────────────────

print(f"Loading: {INPUT_FILE}")
df = pd.read_excel(INPUT_FILE, header=0)
print(f"  Rows: {len(df):,}   Channels: {df.shape[1]}")

# ── Detect spikes ─────────────────────────────────────────────────────────────

spike_mask = pd.Series(False, index=df.index)   # True = this row has a spike

channel_report = {}
for col in df.columns:
    q1  = df[col].quantile(0.25)
    q3  = df[col].quantile(0.75)
    iqr = q3 - q1
    lo  = q1 - IQR_MULTIPLIER * iqr
    hi  = q3 + IQR_MULTIPLIER * iqr

    col_spikes = (df[col] < lo) | (df[col] > hi)
    n_spikes   = col_spikes.sum()

    if n_spikes:
        channel_report[col] = {"count": int(n_spikes), "lo": lo, "hi": hi}

    spike_mask |= col_spikes

spike_rows = df.index[spike_mask].tolist()

# ── Report ────────────────────────────────────────────────────────────────────

print(f"\nSpike detection  (IQR multiplier = {IQR_MULTIPLIER})")
print("-" * 60)
if channel_report:
    for ch, info in channel_report.items():
        print(f"  {ch:<22}  {info['count']:>4} spike(s)   "
              f"normal range [{info['lo']:,.0f}, {info['hi']:,.0f}]")
else:
    print("  No spikes found in any channel.")

print(f"\nTotal spike rows to remove : {len(spike_rows):,}")
print(f"Spike row indices          : {spike_rows}")

# ── Remove spikes (all channels simultaneously) ───────────────────────────────

df_clean = df.drop(index=spike_rows).reset_index(drop=True)
print(f"\nRows after cleaning        : {len(df_clean):,}")
print(f"Rows removed               : {len(df) - len(df_clean):,}")

# ── Save ──────────────────────────────────────────────────────────────────────

df_clean.to_excel(OUTPUT_FILE, index=False)
print(f"\nSaved cleaned file → {OUTPUT_FILE}")
