FROM python:3.10-buster

RUN set -ex \
    && git clone https://github.com/EricBoix/jj_doc_Collecting_Gold_Dust.git \
    # Rename archive for clear context when debugging/fixing in container
    && mv jj_doc_Collecting_Gold_Dust/ jj_doc_Collecting_Gold_Dust.git
    # FIXME: we should be pinning the version with e.g.
    # && cd jj_doc_Collecting_Gold_Dust.git \
    # && git checkout 444b50086c

WORKDIR jj_doc_Collecting_Gold_Dust.git/Convert
RUN set -ex && pip install -r requirements.txt

# Systematically run tests at build time (fail often, fail early)
RUN set -ex \
    && pip install -r requirements-dev.txt \
    && pytest test_main.py

ENTRYPOINT ["python3", "./main.py"]
