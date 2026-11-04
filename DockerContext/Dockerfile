FROM python:3.15

RUN set -ex \
    && git clone https://github.com/EricBoix/jejune_doc_Collecting_Gold_Dust.git \
    # Rename archive for clear context when debugging/fixing in container
    && mv jejune_doc_Collecting_Gold_Dust/ jejune_doc_Collecting_Gold_Dust.git
    # FIXME: we should be pinning the version with e.g.
    # && cd jejune_doc_Collecting_Gold_Dust.git \
    # && git checkout 444b50086c

WORKDIR /jejune_doc_Collecting_Gold_Dust.git/Convert
RUN set -ex && pip install uv

# Installs the locked dependencies, including the tools for running tests
RUN set -ex && uv sync --frozen

ENTRYPOINT ["uv", "run", "--frozen", "main.py"]
