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


api_data = '{"members":{"1552760":{"completion_day_level":{},"id":1552760,"name":null,"local_score":0,"global_score":0,"stars":0,"last_star_ts":0},"1209445":{"last_star_ts":0,"local_score":0,"global_score":0,"stars":0,"completion_day_level":{},"name":"itopal20","id":1209445},"666369":{"name":null,"id":666369,"completion_day_level":{},"global_score":0,"stars":0,"local_score":0,"last_star_ts":0},"973733":{"last_star_ts":1670140334,"completion_day_level":{"3":{"1":{"star_index":569336,"get_star_ts":1670056424},"2":{"star_index":578554,"get_star_ts":1670058814}},"2":{"1":{"star_index":410790,"get_star_ts":1669999516},"2":{"star_index":465856,"get_star_ts":1670016494}},"1":{"2":{"star_index":209697,"get_star_ts":1669958277},"1":{"get_star_ts":1669958069,"star_index":206361}},"4":{"2":{"get_star_ts":1670140334,"star_index":833289},"1":{"star_index":830033,"get_star_ts":1670139414}}},"id":973733,"name":"kbasaran","local_score":42,"global_score":0,"stars":8},"1070351":{"last_star_ts":0,"local_score":0,"stars":0,"global_score":0,"completion_day_level":{},"id":1070351,"name":null},"363672":{"last_star_ts":1670142380,"local_score":46,"stars":8,"global_score":0,"completion_day_level":{"3":{"1":{"get_star_ts":1670057421,"star_index":573130},"2":{"star_index":576064,"get_star_ts":1670058172}},"2":{"2":{"star_index":295716,"get_star_ts":1669973288},"1":{"star_index":292492,"get_star_ts":1669972755}},"4":{"2":{"star_index":840930,"get_star_ts":1670142380},"1":{"star_index":828504,"get_star_ts":1670138955}},"1":{"1":{"star_index":4571,"get_star_ts":1669887748},"2":{"get_star_ts":1669889099,"star_index":10081}}},"id":363672,"name":null},"555438":{"local_score":56,"stars":8,"global_score":0,"completion_day_level":{"2":{"1":{"get_star_ts":1669960592,"star_index":230321},"2":{"star_index":233762,"get_star_ts":1669961265}},"3":{"2":{"get_star_ts":1670052349,"star_index":555331},"1":{"star_index":544088,"get_star_ts":1670048923}},"4":{"2":{"star_index":815950,"get_star_ts":1670135091},"1":{"star_index":812748,"get_star_ts":1670134202}},"1":{"1":{"get_star_ts":1669886681,"star_index":0},"2":{"get_star_ts":1669886858,"star_index":766}}},"name":"Murat Yilmaz","id":555438,"last_star_ts":1670135091}},"event":"2022","owner_id":363672}'
# api_data = '{"members":{"363672":{"completion_day_level":{"5":{"1":{"star_index":916822,"get_star_ts":1638697374},"2":{"star_index":919315,"get_star_ts":1638698436}},"3":{"2":{"get_star_ts":1638516838,"star_index":524852},"1":{"get_star_ts":1638509470,"star_index":495594}},"2":{"2":{"star_index":222781,"get_star_ts":1638421802},"1":{"get_star_ts":1638421469,"star_index":214824}},"21":{"1":{"get_star_ts":1640123304,"star_index":2841649},"2":{"star_index":2844664,"get_star_ts":1640127389}},"17":{"1":{"star_index":2588422,"get_star_ts":1639784942},"2":{"get_star_ts":1639785582,"star_index":2588794}},"10":{"1":{"star_index":1746808,"get_star_ts":1639117232},"2":{"star_index":1768581,"get_star_ts":1639126727}},"4":{"1":{"star_index":753388,"get_star_ts":1638612934},"2":{"get_star_ts":1638613355,"star_index":754385}},"22":{"2":{"star_index":2901126,"get_star_ts":1640212692},"1":{"star_index":2895038,"get_star_ts":1640204093}},"8":{"2":{"get_star_ts":1638999243,"star_index":1556732},"1":{"get_star_ts":1638949250,"star_index":1459105}},"14":{"1":{"get_star_ts":1639483952,"star_index":2278614},"2":{"get_star_ts":1639497174,"star_index":2296597}},"18":{"2":{"get_star_ts":1639844647,"star_index":2627118},"1":{"star_index":2626595,"get_star_ts":1639844101}},"11":{"1":{"star_index":1948065,"get_star_ts":1639246430},"2":{"get_star_ts":1639249528,"star_index":1952671}},"7":{"1":{"get_star_ts":1638865493,"star_index":1291347},"2":{"get_star_ts":1638867167,"star_index":1297164}},"12":{"1":{"get_star_ts":1639315775,"star_index":2037902},"2":{"star_index":2068734,"get_star_ts":1639336360}},"9":{"2":{"get_star_ts":1639028984,"star_index":1596835},"1":{"get_star_ts":1639027494,"star_index":1590161}},"1":{"1":{"get_star_ts":1638335051,"star_index":0},"2":{"star_index":7798,"get_star_ts":1638335775}},"13":{"2":{"star_index":2184193,"get_star_ts":1639415423},"1":{"get_star_ts":1639414230,"star_index":2182330}},"19":{"2":{"star_index":2700492,"get_star_ts":1639947543},"1":{"star_index":2700041,"get_star_ts":1639947088}},"15":{"2":{"get_star_ts":1639563793,"star_index":2370785},"1":{"star_index":2369098,"get_star_ts":1639562354}},"20":{"2":{"get_star_ts":1640042047,"star_index":2777213},"1":{"star_index":2777164,"get_star_ts":1640041987}},"23":{"1":{"get_star_ts":1640295136,"star_index":2944638}},"16":{"1":{"star_index":2488241,"get_star_ts":1639682112},"2":{"star_index":2488716,"get_star_ts":1639682575}},"6":{"1":{"star_index":1081122,"get_star_ts":1638776768},"2":{"get_star_ts":1638776931,"star_index":1081624}}},"id":363672,"last_star_ts":1640295136,"stars":45,"name":null,"global_score":0,"local_score":305},"666369":{"global_score":0,"local_score":0,"stars":0,"name":null,"id":666369,"completion_day_level":{},"last_star_ts":0},"973733":{"global_score":0,"local_score":156,"stars":30,"name":"kbasaran","completion_day_level":{"7":{"2":{"star_index":1387901,"get_star_ts":1638906420},"1":{"get_star_ts":1638905874,"star_index":1386717}},"2":{"2":{"star_index":279380,"get_star_ts":1638433140},"1":{"get_star_ts":1638431810,"star_index":272751}},"9":{"2":{"get_star_ts":1639249140,"star_index":1952070},"1":{"get_star_ts":1639086237,"star_index":1704362}},"12":{"2":{"get_star_ts":1639352345,"star_index":2091591},"1":{"star_index":2083506,"get_star_ts":1639345849}},"5":{"2":{"get_star_ts":1638697132,"star_index":916263},"1":{"star_index":910695,"get_star_ts":1638694640}},"3":{"1":{"get_star_ts":1638518174,"star_index":529675},"2":{"get_star_ts":1638546730,"star_index":621432}},"11":{"1":{"star_index":2063959,"get_star_ts":1639333130},"2":{"get_star_ts":1639333406,"star_index":2064350}},"6":{"1":{"star_index":1182640,"get_star_ts":1638816850},"2":{"get_star_ts":1638863688,"star_index":1285201}},"1":{"1":{"get_star_ts":1638351917,"star_index":54596},"2":{"star_index":58102,"get_star_ts":1638353003}},"10":{"1":{"get_star_ts":1639269702,"star_index":1978115},"2":{"get_star_ts":1639272108,"star_index":1979933}},"13":{"1":{"star_index":2321808,"get_star_ts":1639516041},"2":{"star_index":2321925,"get_star_ts":1639516134}},"4":{"2":{"star_index":753000,"get_star_ts":1638612767},"1":{"get_star_ts":1638610618,"star_index":748318}},"8":{"1":{"star_index":1563805,"get_star_ts":1639003409},"2":{"star_index":1699084,"get_star_ts":1639083130}},"15":{"1":{"get_star_ts":1639860179,"star_index":2641436},"2":{"get_star_ts":1639864483,"star_index":2645454}},"14":{"2":{"star_index":2335638,"get_star_ts":1639530014},"1":{"star_index":2335065,"get_star_ts":1639529086}}},"id":973733,"last_star_ts":1639864483},"1209445":{"completion_day_level":{"2":{"2":{"get_star_ts":1638457307,"star_index":370932},"1":{"star_index":366945,"get_star_ts":1638456205}},"1":{"1":{"star_index":151774,"get_star_ts":1638386716},"2":{"star_index":152633,"get_star_ts":1638387015}},"3":{"2":{"star_index":565355,"get_star_ts":1638527725},"1":{"get_star_ts":1638520941,"star_index":540198}}},"id":1209445,"last_star_ts":1638527725,"name":"itopal20","stars":6,"local_score":18,"global_score":0},"1070351":{"completion_day_level":{"1":{"2":{"star_index":112761,"get_star_ts":1638373260},"1":{"star_index":37777,"get_star_ts":1638346673}}},"id":1070351,"last_star_ts":1638373260,"name":null,"stars":2,"global_score":0,"local_score":8},"1552760":{"completion_day_level":{"5":{"1":{"get_star_ts":1639006733,"star_index":1568107},"2":{"get_star_ts":1639055329,"star_index":1651623}},"11":{"1":{"get_star_ts":1639414849,"star_index":2183264},"2":{"get_star_ts":1639418703,"star_index":2189082}},"3":{"2":{"get_star_ts":1638896407,"star_index":1367050},"1":{"star_index":520691,"get_star_ts":1638515648}},"2":{"2":{"get_star_ts":1638424291,"star_index":241320},"1":{"get_star_ts":1638424072,"star_index":240378}},"7":{"1":{"star_index":1666226,"get_star_ts":1639063630},"2":{"get_star_ts":1639063796,"star_index":1666523}},"12":{"2":{"get_star_ts":1639522585,"star_index":2329863},"1":{"star_index":2329314,"get_star_ts":1639522101}},"9":{"2":{"get_star_ts":1639342132,"star_index":2077791},"1":{"get_star_ts":1639226285,"star_index":1916096}},"10":{"2":{"get_star_ts":1639349199,"star_index":2088142},"1":{"star_index":2082990,"get_star_ts":1639345508}},"1":{"1":{"star_index":26717,"get_star_ts":1638342758},"2":{"star_index":28334,"get_star_ts":1638343425}},"8":{"2":{"get_star_ts":1639212578,"star_index":1892484},"1":{"star_index":1668991,"get_star_ts":1639065196}},"22":{"2":{"star_index":2961230,"get_star_ts":1640336859},"1":{"star_index":2936679,"get_star_ts":1640282190}},"4":{"2":{"get_star_ts":1638998404,"star_index":1555243},"1":{"star_index":1549777,"get_star_ts":1638995500}},"23":{"1":{"get_star_ts":1640597087,"star_index":3055357}},"6":{"1":{"get_star_ts":1639057145,"star_index":1654688},"2":{"star_index":1661387,"get_star_ts":1639060924}}},"last_star_ts":1640597087,"id":1552760,"name":null,"stars":27,"local_score":123,"global_score":0},"555438":{"completion_day_level":{"6":{"1":{"get_star_ts":1638776926,"star_index":1081612},"2":{"get_star_ts":1638778707,"star_index":1086785}},"1":{"1":{"star_index":61456,"get_star_ts":1638354166},"2":{"get_star_ts":1638355322,"star_index":64666}},"13":{"1":{"star_index":2176167,"get_star_ts":1639410321},"2":{"get_star_ts":1639410705,"star_index":2176756}},"10":{"1":{"star_index":1797259,"get_star_ts":1639142598},"2":{"get_star_ts":1639144101,"star_index":1799859}},"4":{"1":{"star_index":786768,"get_star_ts":1638627488},"2":{"star_index":796703,"get_star_ts":1638631944}},"8":{"2":{"get_star_ts":1639005044,"star_index":1566110},"1":{"get_star_ts":1638993676,"star_index":1546364}},"14":{"2":{"get_star_ts":1639524373,"star_index":2331513},"1":{"get_star_ts":1639491927,"star_index":2289316}},"2":{"2":{"get_star_ts":1638426422,"star_index":249654},"1":{"get_star_ts":1638426134,"star_index":248559}},"7":{"1":{"star_index":1361231,"get_star_ts":1638893768},"2":{"star_index":1362592,"get_star_ts":1638894361}},"12":{"2":{"get_star_ts":1639352927,"star_index":2092167},"1":{"get_star_ts":1639348328,"star_index":2086989}},"9":{"2":{"star_index":1709007,"get_star_ts":1639089310},"1":{"get_star_ts":1639037964,"star_index":1618609}},"5":{"2":{"star_index":910832,"get_star_ts":1638694695},"1":{"star_index":907295,"get_star_ts":1638692985}},"3":{"1":{"star_index":532588,"get_star_ts":1638518955},"2":{"star_index":546830,"get_star_ts":1638522662}},"11":{"1":{"star_index":1940492,"get_star_ts":1639241443},"2":{"star_index":1941596,"get_star_ts":1639242159}}},"id":555438,"last_star_ts":1639524373,"stars":28,"name":"Murat Yilmaz","global_score":0,"local_score":161}},"owner_id":363672,"event":"2021"}'
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
width = 6 + max([len(data[1]) for data in member_plot_data.values()]) / 4
height = 1 + 3 * len(member_plot_data)
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
    ax.bar(x, y1, edgecolor=[0, 0, 0, 0.5], color=[0, 0, 0, 0.1])
    ax.bar(x, y2, bottom=y1, edgecolor="k")
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
