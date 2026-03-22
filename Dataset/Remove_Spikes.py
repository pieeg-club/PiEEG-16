"""
EEG Spike Removal Script for PiEEG-16
========================================
Detects and removes/interpolates spikes using robust MAD-based z-score.
Works per-channel, so channels with very different baselines are handled correctly.

Usage:
    python remove_eeg_spikes.py

Outputs:
    output3_clean.xlsx   – cleaned EEG data
    spike_plot_<ch>.png  – before/after plot for each channel that had spikes
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

print ("ok1")


# ── Configuration ─────────────────────────────────────────────────────────────
INPUT_FILE    = "output3.xlsx"
OUTPUT_FILE   = "output3_clean.xlsx"
METHOD        = "mad"       # "mad" (recommended) or "zscore"
THRESHOLD     = 5.0         # spike if score > threshold
REPLACE_WITH  = "interpolate"  # "interpolate" | "median" | "nan"
SAVE_PLOTS    = True
# ──────────────────────────────────────────────────────────────────────────────

print ("ok2")

def mad_zscore(series):
    med = series.median()
    mad = (series - med).abs().median()
    return (series - med).abs() / (1.4826 * mad + 1e-10)

def std_zscore(series):
    return (series - series.mean()).abs() / (series.std() + 1e-10)

def detect_spikes(series):
    score = mad_zscore(series) if METHOD == "mad" else std_zscore(series)
    return score > THRESHOLD

def remove_spikes(series, mask):
    cleaned = series.copy().astype(float)
    cleaned[mask] = np.nan
    if REPLACE_WITH == "interpolate":
        cleaned = cleaned.interpolate(method="linear", limit_direction="both")
    elif REPLACE_WITH == "median":
        cleaned = cleaned.fillna(series.median())
    return cleaned

def plot_channel(original, cleaned, mask, channel):
    fig, axes = plt.subplots(2, 1, figsize=(15, 5), sharex=True)
    t = np.arange(len(original))
    axes[0].plot(t, original.values, lw=0.5, color="steelblue", label="Original")
    spike_idx = np.where(mask.values)[0]
    axes[0].scatter(spike_idx, original.values[spike_idx],
                    color="red", s=12, zorder=5,
                    label=f"Spikes detected: {len(spike_idx)}")
    axes[0].set_title(f"{channel} – Original signal")
    axes[0].legend(fontsize=8)
    axes[0].set_ylabel("Amplitude")
    axes[1].plot(t, cleaned.values, lw=0.5, color="seagreen", label="Cleaned")
    axes[1].set_title(f"{channel} – After spike removal ({REPLACE_WITH})")
    axes[1].legend(fontsize=8)
    axes[1].set_ylabel("Amplitude")
    axes[1].set_xlabel("Sample index")
    plt.suptitle(f"PiEEG-16 | {channel} | method={METHOD}, threshold={THRESHOLD}", fontsize=10, fontweight="bold")
    plt.tight_layout()
    fname = f"spike_plot_{channel.replace('/', '_')}.png"
    plt.savefig(fname, dpi=130)
    plt.close()
    return fname


def main():
    print(f"Loading {INPUT_FILE} …")
    df = pd.read_excel(INPUT_FILE)
    df_clean = df.copy()
    total_spikes = 0
    plots_saved = []

    print(f"\nMethod: {METHOD.upper()}, Threshold: {THRESHOLD}, Replace: {REPLACE_WITH}")
    print(f"{'Channel':<22} {'Spikes':>8}  {'% of data':>10}")
    print("─" * 44)

    for col in df.columns:
        series = df[col]
        mask = detect_spikes(series)
        n = int(mask.sum())
        total_spikes += n
        pct = 100 * n / len(series)
        if n > 0:
            df_clean[col] = remove_spikes(series, mask)
            flag = "  ← cleaned"
            if SAVE_PLOTS:
                fname = plot_channel(series, df_clean[col], mask, col)
                plots_saved.append(fname)
        else:
            flag = ""
        print(f"  {col:<20} {n:>8}   {pct:>8.2f}%{flag}")

    df_clean.to_excel(OUTPUT_FILE, index=False)
    print(f"\n✓ Cleaned data saved → {OUTPUT_FILE}")
    print(f"✓ Total spikes removed across all channels: {total_spikes}")
    if plots_saved:
        print(f"✓ Plots saved: {', '.join(plots_saved)}")

if __name__ == "__main__":
    main()
