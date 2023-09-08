FROM FROM guwenjun/resource-api:v20-sidcar

RUN pip3 install schedule

ADD client_nodes.py /data/run/

CMD ["python3","client_nodes.py"]
