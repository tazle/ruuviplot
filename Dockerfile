FROM resin/rpi-raspbian:stretch

RUN apt-get update && apt-get --no-install-recommends -y install python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install setuptools

COPY requirements.txt /
RUN pip3 install -r requirements.txt
RUN apt-get install --no-install-recommends -y libatlas3-base libfreetype6
RUN mkdir /output

ENTRYPOINT /plot.sh

COPY plot.sh plot-template.json data_for_plot.py plot_data.py /
