FROM python:3.6-alpine

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN apk update && \
    apk add --no-cache python3-dev && \
    pip3 install pipenv && \
    pipenv lock -r > requirements.txt && \
    pip3 uninstall --yes pipenv && \
    pip3 install -r requirements.txt && \
    apk del python3-dev

COPY nowel.py /app/

ENTRYPOINT ["/app/nowel.py"]
