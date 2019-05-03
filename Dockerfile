FROM python:3
ADD . /code
WORKDIR /code
ENV FLASK_DEBUG=0
RUN pip install -r requirements.txt
CMD ["flask" "run" "--host=0.0.0.0"]