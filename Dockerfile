FROM python:3
RUN pip3 install redis
RUN pip3 install pymongo
RUN pip3 install Flask
COPY server.py /
COPY log.config /
VOLUME ["/var/log/"]
EXPOSE 65432
ENTRYPOINT ["python", "server.py"]
