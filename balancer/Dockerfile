FROM python:3
RUN pip3 install redis
RUN pip3 install Flask
RUN pip3 install requests
COPY balancer.py /
VOLUME ["/var/log/"]
EXPOSE 65432
ENTRYPOINT ["python", "balancer.py"]
