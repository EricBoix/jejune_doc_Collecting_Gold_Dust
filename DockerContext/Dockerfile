FROM python:3.10-buster

RUN set -ex \
    && git clone https://github.com/EricBoix/jj_doc_Collecting_Gold_Dust.git \
    && mv jj_doc_Collecting_Gold_Dust/ jj_doc_Collecting_Gold_Dust.git \
    && cd jj_doc_Collecting_Gold_Dust.git
# FIXME: we should be pinning the version
#    && git checkout 444b50086c

WORKDIR jj_doc_Collecting_Gold_Dust.git/Convert
RUN set -ex \
    && pip install -r requirements.txt

RUN ls -al

RUN set -ex \
    && pip install -r requirements-dev.txt \
    && pytest test_main.py

COPY ./entrypoint.py ./

ENTRYPOINT ["python3", "./entrypoint.py"]
CMD ["--help"]
