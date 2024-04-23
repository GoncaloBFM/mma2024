FROM python:3
WORKDIR /usr/src/app
ADD ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH="$PYTHONPATH:$PWD"
CMD ["python", "./src/main.py"]