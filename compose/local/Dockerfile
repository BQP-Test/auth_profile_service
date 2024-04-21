FROM python:3.10

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential



#APP Setup

WORKDIR /app

COPY src/requirements.txt .

RUN pip install -r requirements.txt

COPY ./compose/local/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


COPY . .

EXPOSE 6001
