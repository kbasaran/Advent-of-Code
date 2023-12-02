import matplotlib.pyplot as plt
import datetime as dt
import json

BASE_SIZE = 70

with open("data.json") as f:
    data = json.loads(f.read())

year = int(data["event"])
processed_data = {}
leaderboard = data["members"][str(data["owner_id"])]["name"] or data["owner_id"]

def day_start(day: int):
    return dt.datetime.strptime(f'2022 12 {day:02d} 05', "%Y %m %d %H")

for member_id in data["members"]:
    member_day_parts = []
    member_day_times = []
    member_data = data["members"][member_id]
    key = member_data["name"] or member_id
    completion_data = member_data["completion_day_level"]
    for i in completion_data:
        for j in completion_data[i]:
            completion_time = dt.datetime.utcfromtimestamp(completion_data[i][j]["get_star_ts"])
            timediff = (completion_time - day_start(int(i))).total_seconds() / 3600
            if timediff <= 24:
                member_day_times.append(timediff)
                member_day_parts.append(int(i) + 0.20 * (2 * int(j) - 3))
    if len(member_day_parts):
        processed_data[key] = (member_day_parts, member_day_times)

def format_y(y, p):
    return f'{y:2.0f}:00:00'

c1 = "#123"  # bg color 1
c2 = "#1b2b3b"  # bg color 2
ct = "#e6d418"  # label text color

fig = plt.figure(facecolor=c1, figsize=(20, 9))
ax = fig.add_subplot(1, 1, 1)
ax.set_facecolor(c2)
ax.set_yticks(list(range(0,25,4)))
ax.set_yticklabels(list(range(0,25,4)), color=ct, fontsize=10)
ax.yaxis.set_major_formatter(plt.FuncFormatter(format_y))
ax.tick_params('both', length=0, width=0, which='minor')
ax.tick_params('both', length=0, width=0, which='major')
ax.set_xticks([ x for x in range(1, 26)])
ax.set_xticklabels([f'{i}' for i in range(1, 26)], color=ct, fontsize=10)

for i in range(0, 13):
    ax.axvspan((2 * i - 1) + 0.5, (2 * i - 1) + 1.5, facecolor=c1)
    ax.axvspan(2 * i + 0.5, 2 * i + 1.5, facecolor=c2)

data = tuple(processed_data.values())
groups = tuple(processed_data.keys())
colors = ("#f33", "#cc3", "#66f", "#a83", "cyan", "yellow")
colors = ["#31bf73", "#f6e418", "#38eafb", "#cfa2b8", "#2f81f7", "#f8a925", "#ccc", "#d33"] * 8
markers = ["d", "*", "v", "X", "^", "D", "s", "o", "h"] * 9

for data, color, group, marker in zip(data, colors, groups, markers):
    marker_dict = {
            "363672" : "$\\mathbf{\\lambda}}$",
            "Murat Yilmaz" : "$\\mathbf{\\#}}$",
            }
    mrkr = marker_dict.get(group, marker)
    size_dict = {"*" : 2, "D" : 0.7, "s" : 0.7, "$\\mathbf{\\lambda}}$" : 1.4, "X" : 1.2, "P" : 1.2}
    size = size_dict.get(mrkr, 1) * BASE_SIZE
    x, y = data
    ax.scatter(x, y, alpha=0.7, c=color, edgecolors='none', s=size, label=group, marker=mrkr)

ax.set_xlim(0.5, 25.5)
ax.set_ylim(24, -0.1)
ax.legend(loc='lower left', bbox_to_anchor= (1, 0.7), ncol=1,
            borderaxespad=0, frameon=False, labelcolor=colors)

plt.title(f"{leaderboard}'s Advent of Code Leaderboard - {year}", color=ct, size=16)
plt.savefig('plot.png', dpi=200, pad_inches=0.5, bbox_inches="tight")