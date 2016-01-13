FROM python:3.5-slim
ADD index.html /srv/index.html
WORKDIR /srv
CMD [ "python", "-m", "http.server", "80" ]
