FROM python:3.7

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com \
    && python manage.py collectstatic --noinput

CMD ["uwsgi", "--ini", "uwsgi.ini"]