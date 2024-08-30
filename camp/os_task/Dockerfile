FROM python:3.12-slim-bookworm


WORKDIR /app/
COPY . /app/
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
  pip install -r requirements.txt && \
  rm -rf /root/.cache/pip

ENTRYPOINT [ "python", "converter.py" ]
