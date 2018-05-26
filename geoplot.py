"""
Plots locations of source and destination from a firewall log. This takes a
destination IP and plots all sources to that destination. The width of the line
indicates quantity.
"""
import argparse
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import re
from geolite2 import geolite2


def main(args):
    """
    Main for geoplot.py
    :param args:
    :return:
    """
    events = {}
    src_patt = re.compile("SRC=(.+?)\s")
    dst_patt = re.compile("DST=(.+?)\s")
    print(args)
    rd = geolite2.reader()
    ipl = rd.get(args.DST_IP)
    dlon = ipl['location']['longitude']
    dlat = ipl['location']['latitude']

    with open(args.LOG_FILE, 'r') as infile:
        for line in infile.readlines():
            try:
                dst = dst_patt.findall(line)[0]
            except IndexError:
                continue
            if args.DST_IP == dst:
                src = src_patt.findall(line)[0]
                if src in events:
                    events[src] += 1
                else:
                    events[src] = 1

    fig = plt.figure()
    m = Basemap(resolution='l',
                projection='mill', lon_0=0)
    m.drawcoastlines()
    m.fillcontinents()
    m.drawcountries()

    for evt in events:
        ipl = rd.get(evt)
        lat = ipl['location']['latitude']
        long = ipl['location']['longitude']
        m.plot(long, lat, 'ro', latlon=True, zorder=3,
               markersize=events[evt] / 2)

    m.plot(dlon, dlat, 'go', latlon=True, zorder=2, markersize=4)
    geolite2.close()

    plt.show()


if __name__ == "__main__":
    des = "Plots source ip locations given a destination IP."
    PARSER = argparse.ArgumentParser(description=des)
    PARSER.add_argument('DST_IP', help="Destination IP to use")
    PARSER.add_argument('LOG_FILE', help='Log file to parse')
    ARGS = PARSER.parse_args()
    main(ARGS)
