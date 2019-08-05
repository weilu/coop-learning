FROM python:3

# prep graph-tool download
RUN echo 'deb http://downloads.skewed.de/apt/buster buster main' >> /etc/apt/sources.list
RUN echo 'deb-src http://downloads.skewed.de/apt/buster buster main' >> /etc/apt/sources.list
RUN apt-key adv --keyserver keys.openpgp.org --recv-key 612DEFB798507F25
# install graph-tool
RUN apt-get update
RUN apt-get install -y python3-graph-tool

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# add default python package dir to path (needed for graph-tool)
ENV PYTHONPATH "$PYTHONPATH:/usr/lib/python3/dist-packages/"

# CMD [ "python", "-m", "unittest", "discover", "."]
