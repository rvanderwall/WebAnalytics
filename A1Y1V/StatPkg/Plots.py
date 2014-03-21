__author__ = 'robert'

import datetime
import re
import numpy as np
import matplotlib.pyplot as plt

import A1Y1V.Records.FieldNames as fn


def plot_data_over_TOD(collection):
    data = []
    for hour in range(0, 24):
        print("Hour:{0}").format(hour)
        for minute in range(0, 60):
            start = 60 * (hour * 60 + minute)
            end = start + 60
            resp = collection.find(
                {fn.ACTIVITY_TIME: {"$gte": start, "$lt": end}}).distinct(fn.USER_IP)
            data.append(len(resp))

    #time_axis = np.arange(0, len(data) / 60, 1.0 / 60)
    time_axis = np.arange(0, 24, 1.0 / 60)
    plt.plot(time_axis, data)
    plt.title("Hits Per Minute")
    plt.ylabel("Number of Hits From Unique IPs")
    plt.xlabel("Time - 24hr Format - In GMT-0")
    plt.show()
