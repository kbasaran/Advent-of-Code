#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 09:01:28 2022

@author: kerem
"""

import pandas as pd
import datetime
import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np
plt.rcParams["figure.dpi"] = 150


api_data = ''
df = pd.read_json(api_data)

member_plot_data = {}
for i, row in df.iterrows():
    if row.members["local_score"] == 0:
        continue
    if (name := row.members["name"]) is None:
        name = row.name

    member_plot_data[name] = {1: {}, 2: {}}    
    for day_str, data in row.members["completion_day_level"].items():
        day = int(day_str)
        data = {int(key): val for key, val in data.items()}
        day_start_ts = datetime.datetime(df.iloc[0, :].event, 12, int(day), 6, 0).timestamp()
        member_plot_data[name][1][day] = (data.get(1, {"get_star_ts": day_start_ts + 24 * 60 * 60}).get("get_star_ts") - day_start_ts) / 60 / 60
        member_plot_data[name][2][day] = (data.get(2, {"get_star_ts": day_start_ts + 24 * 60 * 60}).get("get_star_ts") - day_start_ts) / 60 / 60

    member_plot_data[name][1] = OrderedDict(sorted(member_plot_data[name][1].items()))
    member_plot_data[name][2] = OrderedDict(sorted(member_plot_data[name][2].items()))


# First method
width = 4 + max([len(data[1]) for data in member_plot_data.values()]) / 4
height = 1 + 2 * len(member_plot_data)
plt.rcParams["figure.figsize"] = [width, height]

fig, axs = plt.subplots(len(member_plot_data), sharex=True)
fig.suptitle(f"----AoC Year {df.iloc[0, :].event}----")

x_max = 0
for i, ax in enumerate(axs):
    member_name = list(member_plot_data.keys())[i]
    member_data = member_plot_data[member_name]
    ax.set_ylim([0, 24])
    ax.grid()
    ax.set_title(member_name)
    y1 = list(member_data[1].values())
    y2 = list(member_data[2].values())
    x = list(member_data[1].keys())
    x_max = max(x_max, *x)
    ax.bar(x, np.ones(len(x)) * 24, bottom=y2, color=[0.6, 0.8, 0.6], edgecolor=[0.25, 0.25, 0.25])
    ax.bar(x, y1, color=[0, 0, 0, 0.1], edgecolor=[0.25, 0.25, 0.25])
    ax.bar(x, y2, bottom=y1, edgecolor=[0.25, 0.25, 0.25])
    ax.set_ylabel("Hour")

ax.set_xlabel("Day")
plt.xticks(list(range(1, x_max+1)))
fig.tight_layout()
plt.show()


# Second method
width = 6 + max([len(data[1]) for data in member_plot_data.values()])
height = 8
plt.rcParams["figure.figsize"] = [width, height]

ax = plt.subplot()
ax.set_title(f"----AoC Year {df.iloc[0, :].event}----")

x_max = 0
n_members = len(member_plot_data.keys())
width = 0.7 / n_members
for i, member_name in enumerate(member_plot_data.keys()):
    member_data = member_plot_data[member_name]
    y1 = list(member_data[1].values())
    y2 = list(member_data[2].values())
    x = list(member_data[1].keys())
    x_label_center_locs = np.arange(len(x)) + 1
    x_max = max(x_max, *x)
    ax.bar(x_label_center_locs - width / 2 * (n_members - 1) + i * width,
            y1,
            width,
            edgecolor=[0, 0, 0, 0.5],
            color=[0, 0, 0, 0.1],
            )
    ax.bar(x_label_center_locs - width / 2 * (n_members - 1) + i * width,
            y2,
            width,
            bottom=y1,
            label=member_name,
            edgecolor="k",
            )

ax.set_ylabel("Hour")
ax.set_xlabel("Day")
ax.set_ylim([0, 24])
ax.grid()
ax.legend()
plt.xticks(list(range(1, x_max+1)))
