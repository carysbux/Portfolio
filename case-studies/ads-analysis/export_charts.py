#!/usr/bin/env python3
"""Build static chart PNGs for the case study from ads-analysis dashboard/data.json."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Resolve data.json: prefer env ADS_DATA_JSON; else repo next to case-studies; else Documents/Github.
_HERE = Path(__file__).resolve().parent
_candidates = [
    Path(os.environ.get("ADS_DATA_JSON", "")),
    _HERE.parent.parent / "Github" / "ads-analysis" / "dashboard" / "data.json",
    Path.home() / "Documents" / "Github" / "ads-analysis" / "dashboard" / "data.json",
    Path("/Users/Carys/Documents/Github/ads-analysis/dashboard/data.json"),
]
DATA_JSON = next((p for p in _candidates if p and p.is_file()), None)
OUT = _HERE / "assets"
COLORS = {
    "Google Ads": "#1f77b4",
    "Meta Ads": "#ff7f0e",
    "TikTok Ads": "#2ca02c",
}
BAR_CPC = "#4C78A8"
BAR_CPA = "#F58518"
BAR_ROAS = "#4C78A8"


def main() -> None:
    if DATA_JSON is None:
        print("Could not find dashboard/data.json. Set ADS_DATA_JSON=/path/to/data.json", file=sys.stderr)
        sys.exit(1)

    os.environ.setdefault("MPLCONFIGDIR", str(_HERE / ".mplcache"))
    Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)

    curves = data.get("platform_spend_bin_curves") or []
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.2))
    for c in curves:
        col = COLORS.get(c["platform"], "#333333")
        pts = c["points"]
        x = [p["mean_spend"] for p in pts]
        y_rev = [p["mean_revenue"] for p in pts]
        y_rpd = [p["revenue_per_dollar"] for p in pts]
        ax1.plot(x, y_rev, marker="o", label=c["platform"], color=col, linewidth=2)
        ax2.plot(x, y_rpd, marker="o", label=c["platform"], color=col, linewidth=2)
    ax1.set_xlabel("Average spend per bin (USD)")
    ax1.set_ylabel("Average revenue per bin (USD)")
    ax1.set_title("Spend vs revenue (by platform)", fontweight="600")
    ax1.legend(title="Platform")
    ax1.grid(True, alpha=0.35)
    ax2.set_xlabel("Average spend per bin (USD)")
    ax2.set_ylabel("Revenue per $1 spend")
    ax2.set_title("Revenue per $1 spend by bin (by platform)", fontweight="600")
    ax2.legend(title="Platform")
    ax2.grid(True, alpha=0.35)
    fig.suptitle("Quantile bins of ad_spend per platform (q=10)", fontsize=10, color="#444")
    fig.tight_layout()
    fig.savefig(OUT / "chart_spend_revenue_bins.png", dpi=160, bbox_inches="tight")
    plt.close()

    panels = data.get("roas_best_by_platform_industry") or []
    y_max = 0.0
    for panel in panels:
        for row in panel.get("rows") or []:
            y_max = max(y_max, float(row.get("best_group_roas") or 0))
    y_max = y_max * 1.15 if y_max > 0 else 1.0

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)
    for ax, panel in zip(axes, panels):
        rows = panel.get("rows") or []
        labels = [r["industry"] for r in rows]
        vals = [float(r["best_group_roas"]) for r in rows]
        ax.bar(labels, vals, color=BAR_ROAS, edgecolor=BAR_ROAS, linewidth=0.5)
        ax.set_title(panel.get("platform", ""), fontweight="600")
        ax.set_ylim(0, y_max)
        ax.tick_params(axis="x", rotation=35, labelsize=9)
        ax.set_ylabel("Best group ROAS")
        ax.grid(True, axis="y", alpha=0.35)
    fig.suptitle("Best group ROAS by industry (winning campaign type per platform)", fontsize=11, color="#333")
    fig.tight_layout()
    fig.savefig(OUT / "chart_roas_by_platform.png", dpi=160, bbox_inches="tight")
    plt.close()

    rows_c = sorted(
        data.get("platform_avg_cpc_cpa") or [],
        key=lambda r: r["avg_CPA"],
        reverse=True,
    )
    labels_p = [r["platform"] for r in rows_c]
    cpc = [r["avg_CPC"] for r in rows_c]
    cpa = [r["avg_CPA"] for r in rows_c]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    x_idx = range(len(labels_p))
    w = 0.35
    ax.bar([i - w / 2 for i in x_idx], cpc, width=w, label="Avg CPC", color=BAR_CPC)
    ax.bar([i + w / 2 for i in x_idx], cpa, width=w, label="Avg CPA", color=BAR_CPA)
    ax.set_xticks(list(x_idx))
    ax.set_xticklabels(labels_p)
    ax.set_ylabel("Value (USD)")
    ax.set_title("Average CPC & CPA by platform", fontweight="600")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.35)
    fig.tight_layout()
    fig.savefig(OUT / "chart_cpc_cpa_bars.png", dpi=160, bbox_inches="tight")
    plt.close()

    pts = data.get("platform_avg_cpc_cpa") or []
    fig, ax = plt.subplots(figsize=(6.5, 5))
    for r in pts:
        p = r["platform"]
        ax.scatter(
            r["avg_CPC"],
            r["avg_CPA"],
            s=220,
            c=COLORS.get(p, "#6b7280"),
            edgecolors="white",
            linewidths=1.2,
        )
        ax.annotate(p.replace(" Ads", ""), (r["avg_CPC"], r["avg_CPA"]), fontsize=9, xytext=(6, 6), textcoords="offset points")
    ax.set_xlabel("Avg CPC ($)")
    ax.set_ylabel("Avg CPA ($)")
    ax.set_title("Avg CPC vs avg CPA", fontweight="600")
    ax.grid(True, alpha=0.35)
    fig.tight_layout()
    fig.savefig(OUT / "chart_cpc_cpa_scatter.png", dpi=160, bbox_inches="tight")
    plt.close()

    print(f"Wrote charts to {OUT} (source {DATA_JSON})")


if __name__ == "__main__":
    main()
