from python:2.7

COPY app /opt/heimdal
COPY run_heimdal.sh /

RUN pip install -r /opt/heimdal/requirements.txt

CMD ["/run_heimdal.sh"]