# Where the document comes from: "remote" (git clone from GitHub, the default)
# or "local" (jejune_cli passes --build-context jejune-doc=<local clone>).
ARG DOC_SOURCE=remote
# Where pdf-to-markdown comes from: "locked" (the uv.lock version, the default)
# or "local" (jejune_cli passes --build-context pdf-to-markdown=<local checkout>).
ARG PDF_TO_MARKDOWN_SOURCE=locked

FROM python:3.15 AS remote-doc

RUN set -ex \
    && git clone https://github.com/EricBoix/jejune_doc_Collecting_Gold_Dust.git \
    # Rename archive for clear context when debugging/fixing in container
    && mv jejune_doc_Collecting_Gold_Dust/ jejune_doc_Collecting_Gold_Dust.git
    # FIXME: we should be pinning the version with e.g.
    # && cd jejune_doc_Collecting_Gold_Dust.git \
    # && git checkout 444b50086c

FROM python:3.15 AS local-doc
COPY --from=jejune-doc / /jejune_doc_Collecting_Gold_Dust.git

FROM ${DOC_SOURCE}-doc AS doc

# Empty unless jejune_cli provides a local pdf-to-markdown
FROM scratch AS locked-pdf-to-markdown

FROM scratch AS local-pdf-to-markdown
COPY --from=pdf-to-markdown / /

FROM ${PDF_TO_MARKDOWN_SOURCE}-pdf-to-markdown AS pdf-to-markdown-source

FROM doc
ARG PDF_TO_MARKDOWN_SOURCE
COPY --from=pdf-to-markdown-source / /pdf-to-markdown

WORKDIR /jejune_doc_Collecting_Gold_Dust.git/Convert
RUN set -ex && pip install uv

# A local pdf-to-markdown replaces the git source of pyproject.toml (and the
# locked version): the lock is rewritten inside the image only.
RUN set -ex && if [ "${PDF_TO_MARKDOWN_SOURCE}" = "local" ]; then uv add /pdf-to-markdown; fi

# Installs the locked dependencies, including the tools for running tests
RUN set -ex && uv sync --frozen

ENTRYPOINT ["uv", "run", "--frozen", "main.py"]
