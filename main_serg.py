from collections import defaultdict, OrderedDict
from datetime import datetime
from typing import Dict

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random


def get_rand_color() -> str:
    r = lambda: random.randint(0, 255)

    return '#%02X%02X%02X' % (r(), r(), r())


def draw_graph(rates: Dict) -> None:
    plt.rcParams['figure.figsize'] = (35, 20)
    subplot = plt.subplot()

    handles = []

    for theme, v in rates.items():
        ordered_dict = OrderedDict()

        for i in sorted(v.keys()):
            ordered_dict[i] = v[i]

        axis_x = ordered_dict.keys()
        axis_y = ordered_dict.values()

        color = get_rand_color()
        subplot.plot(axis_x, axis_y, c=color)
        patch = mpatches.Patch(color=color, label=' '.join(theme))
        handles.append(patch)

    plt.legend(handles=handles)

    plt.xlabel("Количество запросов по теме")
    plt.ylabel("Время")
    plt.title("Поисковые запросы")

    plt.savefig('pic.png')
    plt.clf()


def main(log_file_name: str) -> None:
    df = pd.read_csv(log_file_name, sep='\t')

    score = defaultdict(lambda: defaultdict(int))
    themes = [  # naive implementation
        ('чм', 'чемпионат'),
        ('хостел', 'отель', 'гостиница', 'снять жильё', 'снять квартиру'),
        ('счёт', 'счет'),
        ('ставки', 'букмеркер', 'букмекерская'),
        ('трансляция', 'матч'),
        ('футбол', 'сборная'),
        ]

    for i, row in df.iterrows():
        query = row['normal_query']
        query_dt = str(datetime.fromisoformat(row['datetime']).date())

        for theme in themes:
            for theme_word in theme:
                if not isinstance(query, str):
                    continue
                if query.find(theme_word) != -1:

                    score[theme][query_dt] += 1
    draw_graph(score)


main('log')
