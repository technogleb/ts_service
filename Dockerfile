FROM python:3.6
WORKDIR /app
ENV PYTHONPATH=/app
COPY app/ /app
RUN cd ts_core && python setup.py install && \
    cd ../ && pip install -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "src:create_app()"]
