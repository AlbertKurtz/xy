"""Temporal fills retain date ticks, share units, and remove every region."""

from datetime import datetime, timedelta

import numpy as np

import xy.pyplot as plt

dates = [datetime(2026, 1, 1) + timedelta(days=i) for i in range(7)]
upper = np.array([3.0, 4.0, 5.0, 4.0, 6.0, 5.0, 7.0])
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
axes[0].fill_between(dates, upper, upper - 2.0, alpha=0.35)
axes[0].set_title("Python datetime band")
axes[1].fill_between(np.asarray(dates, dtype="datetime64[D]"), upper, step="mid", alpha=0.35)
axes[1].set_title("NumPy datetime steps")
masked_dates = np.ma.masked_array(dates, mask=[False, False, False, True, False, False, False])
axes[2].fill_between(masked_dates, upper, alpha=0.35)
axes[2].set_title("Masked datetime gaps")

shared_fig, shared_axes = plt.subplots(2, 1, sharex=True, figsize=(7, 6))
shared_axes[1].axhline(1, color="purple")
# Render before adding dates to exercise shared-axis cache refresh.
shared_fig.canvas.draw()
shared_axes[0].fill_between(masked_dates, upper, alpha=0.35)
shared_axes[0].set_title("Shared dates: labels on the panel without date data")

replacement_fig, replacement_ax = plt.subplots()
removed = replacement_ax.fill_between(masked_dates, upper)
replacement_fig.canvas.draw()
removed.remove()
replacement_ax.fill_between([0, 1, 2], [1, 2, 1], alpha=0.35)
# Matplotlib retains removed artists' data limits until explicitly reset.
replacement_ax.set_xlim(-0.1, 2.1)
replacement_ax.set_ylim(0, 3)
replacement_ax.set_title("All date regions removed: numeric replacement")
