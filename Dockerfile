FROM python:3.6
WORKDIR /app
ENV PYTHONPATH=/app
COPY app/ /app
RUN cd ts_core && python setup.py install && \
    cd ../ && pip install -r requirements.txt

CMD python src/app.py
