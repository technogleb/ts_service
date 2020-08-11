FROM python:3.6
WORKDIR /ts_service
ENV PYTHONPATH=/ts_service
COPY ts_service/ /ts_service
COPY ts_core/ /ts_core
RUN cd /ts_core && python setup.py install && \
    cd /ts_service && pip install -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "ts_service:create_app()"]
