import math

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import numpy.polynomial.polynomial as poly

from imdb_scraper.IMDb import IMDB_Web_Scrape


def get_regression_line(time, points):
    return poly.polyval(time, poly.polyfit(time, points, 1))


def scrape_imdb(ax, id, seasons, name=None, ylim=None):
    try:
        pd.read_csv(f"{id}.csv").reset_index()
    except FileNotFoundError:
        data = IMDB_Web_Scrape(id, seasons).pull_seasons()
        data.to_csv(f"{id}.csv")
    finally:
        # without this trick, all ratings etc are 'bs4.element.NavigableString', which are weird
        data = pd.read_csv(f"{id}.csv").reset_index()

    ax.set_xticks(range(0, len(data)))
    ax.set_xticklabels([f'S{row["Season"]}E{row["Episode"]}' for _, row in data.iterrows()])
    plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

    #ax.set_xlabel('Episodes')
    ax.set_ylabel('IMDB Ratings')

    if ylim is not None:
        ax.set_ylim(ylim)
    else:
        upper_limit = math.ceil(max(data["IMDB Rating"]))
        lower_limit = math.floor(min(data["IMDB Rating"]))
        ax.set_ylim((lower_limit, upper_limit))

    if name is not None:
        ax.set_title(name)

    for i in range(1, max(data["Season"]) + 1):
        season = data[data["Season"] == i]
        index = np.array(season["index"])
        ratings = np.array(season["IMDB Rating"])
        reg = get_regression_line(index, ratings)
        ax.scatter(index, ratings)
        ax.plot(index, reg, label=f"Season: {i}")

    legend = ax.legend(loc='lower right')
    legend.get_frame().set_facecolor('C0')

    return ax


if __name__ == "__main__":
    fig, axes = plt.subplots(2, 1)

    scrape_imdb(axes[0], "tt0417299", 3, "ALTA", (6,10))
    scrape_imdb(axes[1], "tt1695360", 4, "Korra", (6,10))

    plt.show()

    fig.savefig("Avatar_and_Korra.png", dpi=300)
