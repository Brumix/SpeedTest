FROM python:3

WORKDIR /home/pi/Documents/

COPY main.py .

RUN pip3 install matplotlib
RUN pip3 install pandas
RUN pip3 install speedtest-cli
