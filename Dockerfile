from python:2.7

COPY app /opt/heimdal
COPY run_heimdal.sh /

RUN pip install -r /opt/heimdal/requirements.txt

ENV RULES_FILE /opt/heimdal/rules.json

CMD ["/run_heimdal.sh"]
