'''
Made by:
	Bruno Pereira
	38054@ufp.edu.pt
'''


import datetime
import os
import time

import matplotlib.pyplot as plt
import pandas as pd
import speedtest
from calendar import monthrange

WORKING_DIRECTORY = 'data/'
INFO_EXTENSION = '.csv'
IMAGE_EXTENSION = '.png'
INTERVAL = 3600


def file_name() -> str:
    if not os.path.exists(WORKING_DIRECTORY):
        os.mkdir(WORKING_DIRECTORY)
    directory = WORKING_DIRECTORY + datetime.datetime.today().strftime('%b%Y') + '/'
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory + datetime.datetime.today().strftime('%b%Y-%d')


def config_best_speed_test():
    s = speedtest.Speedtest()
    s.get_config()
    s.get_best_server()
    return s


def get_time() -> str:
    time = datetime.datetime.now()
    return time.strftime('%H:%M')


def get_mounth() -> str:
    time = datetime.datetime.now()
    return time.strftime('%b%Y')


def get_download(s) -> float:
    speed_bps = s.download()
    speed_mbps = round(speed_bps / 1000 / 1000, 1)
    return speed_mbps


def get_upload(s) -> float:
    speed_bps = s.upload()
    speed_mbps = round(speed_bps / 1000 / 1000, 1)
    return speed_mbps


def get_ping(s) -> float:
    ping = s.results.ping
    return round(ping, 3)


def store_values_csv(timeupdate, download, upload, ping, filename=file_name() + INFO_EXTENSION):
    exits = False
    if os.path.exists(filename):
        exits = True
    values = pd.DataFrame([[timeupdate, download, upload, ping]],
                          columns=['Time', 'Download', 'Upload', 'Ping'])
    if exits:
        values.to_csv(filename, index=False, mode='a', header=False)
        return
    values.to_csv(filename, index=False, mode='a', header=True)
    return


def make_graph(filename):
    df = pd.read_csv(filename)
    plt.figure(1, (10, 10))
    plt.title('Net Speed')
    plt.xlabel('Time')
    plt.ylabel('MBPS')
    plt.plot(df['Time'], df['Download'], label='Download')
    plt.plot(df['Time'], df['Upload'], label='Upload')
    plt.plot(df['Time'], df['Ping'], label='Ping')
    plt.grid(True)
    plt.legend()
    plt.savefig(name_image())
    plt.show()


def name_image() -> str:
    return file_name() + IMAGE_EXTENSION


def net_speed():
    s = config_best_speed_test()
    time = get_time()
    download_speed = get_download(s)
    upload_speed = get_upload(s)
    ping = get_ping(s)
    print(f" Time: {time}  Download:{download_speed} mbps Upload:{upload_speed} mbps Ping:{ping}")
    store_values_csv(time, download_speed, upload_speed, ping)


def timer():
    now = datetime.datetime.now()
    midnight = now.replace(hour=00, minute=0, second=0, microsecond=0)
    midnight_delay = now.replace(hour=00, minute=10, second=0, microsecond=0)
    net_speed()
    if midnight <= now <= midnight_delay:
        make_graph(file_name() + INFO_EXTENSION)


def last_day_of_month(date_value):
    return date_value.replace(day=monthrange(date_value.year, date_value.month)[1])


def last_day():
    if datetime.datetime(2021, 4, 30).date() == last_day_of_month(datetime.datetime.today().date()) \
            and datetime.datetime.now().hour == 23:
        path = os.walk(WORKING_DIRECTORY + datetime.datetime.today().strftime('%b%Y') + '/')
        for path, _, files in path:
            for file in files:
                if file.find(INFO_EXTENSION) != -1:
                    average_file(os.path.join(path, file))


def get_avg(dictionary, data, key):
    total = 0
    summered = 0
    for d in data:
        total += 1
        summered += d
    dictionary[key] = round(summered / total, 4)


def average_file(filename):
    store_file = WORKING_DIRECTORY + get_mounth() + '/' + get_mounth() + INFO_EXTENSION
    data = dict()
    file = pd.read_csv(filename)
    get_avg(data, file['Download'], 'Download')
    get_avg(data, file['Upload'], 'Upload')
    get_avg(data, file['Ping'], 'Ping')
    store_values_csv(get_mounth(), data['Download'], data['Upload'], data['Ping'], store_file)
    make_graph(store_file)


def main():
    last_day()
    timer()


if __name__ == '__main__':
    print('APP STARTING ...')
    main()
