FROM python:3.9


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./ /code/


RUN python /code/initialize.py


EXPOSE 5000


CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]

