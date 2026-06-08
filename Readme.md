# Extracting the book semantic structure out of Collecting Gold Dust book<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [Running the converter](#running-the-converter)
- [Running the PDF conversion with docker](#running-the-pdf-conversion-with-docker)
- [Running the full data workflow](#running-the-full-data-workflow)
- [Development](#development)

## Introduction

This directory holds a [copy of the pdf version of Sayadaw U Tejaniya's book
COLLECTING GOLD DUST Nurturing the Dhamma in Daily Living](./original_data/2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1.pdf) as offered e.g. by [this Scribd link](https://www.scribd.com/document/716383730/Collecting-Gold-Dust-Web-Book-1)

## Running the converter

```bash
cd `git rev-parse --show-toplevel`/Convert
python3.10 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Running the PDF conversion with docker

```bash
docker build -tjejuness:doc_Collecting_Gold_Dust https://github.com/EricBoix/jj_doc_Collecting_Gold_Dust.git#:DockerContext
docker run --rm jejuness:doc_Collecting_Gold_Dust --help
```

Extracting the result out of the container requires local filesystem mount

```bash
docker run --rm  -v `pwd`/junk:/output jejuness:doc_Collecting_Gold_Dust --output_directory /output
```

## Running the full data workflow

From original PDF to markdown and JSON

```bash
cd `git rev-parse --show-toplevel`
docker build -tjejuness:doc_Collecting_Gold_Dust https://github.com/EricBoix/jj_doc_Collecting_Gold_Dust.git#:DockerContext
docker run --rm  -v `pwd`/result_data:/output jejuness:doc_Collecting_Gold_Dust --output_directory /output
```

Prerequisite Knowledge Graph (KG) extraction: launch a neo4j database

```bash
cd `git rev-parse --show-toplevel`
docker build -t jejuness:jj_neo4j_docker https://github.com/EricBoix/jj_neo4j_docker.git
# Note: are we missing -e NEO4J_dbms_security_procedures_unrestricted: "apoc.*" \
docker run --rm --detach --name jj_neo4j_db \
    --publish=7474:7474 --publish=7687:7687 \
    --env NEO4J_AUTH=neo4j/your_password \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -v `pwd`/result_data/database:/data \
    jejuness:jj_neo4j_docker
# Transmitting required info to following DB process users
echo "# Neo4j server designation and associated credentials" > .env
echo "NEO4J_URI=bolt://localhost:7687"                       >> .env
echo "NEO4J_USERNAME=neo4j"                                  >> .env
echo "NEO4J_PASSWORD=your_password"                          >> .env
```

Configure the KG (Knowledge Graph) extraction

```bash
if [ ! -f .env ]; then
  echo ".env file with DB info does not exist. Exiting."
  return
fi
# Configuring the llm model to be used
echo "### LLM server designation and associate credential"      >> .env
echo "MODEL_URL=https://ollama-ui.pagoda.liris.cnrs.fr/ollama/" >> .env
echo "API_KEY=sk-dde3f395ce1b4bfcb5c0d7f4c46b9c0c"              >> .env
echo "MODEL=llama3:70b"                                         >> .env
```

Run the (Knowledge Graph) extraction

```bash
docker build -t jejuness:jj_build_knowledge_graph https://github.com/EricBoix/jj_build_knowledge_graph.git#:DockerContext
docker run --rm --tty --name jj_build_knowledge_graph \
  -v `pwd`/result_data:/data \
  --env-file .env \
  jejuness:jj_build_knowledge_graph extracting_graph_semantic_chuncker.py --input_directory /data \
  --load_markdown_document 2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1_-_local_converter.md \
  --load_json_document 2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1_-_Sentences_as_LangChain_Document.json
```

Dump the database content for later usage

```bash
# Dumping requires the DB to be halted properly
docker stop $(docker ps -q --filter ancestor=jejuness:jj_neo4j_docker )
docker run --interactive --tty --rm  \
    --volume=`pwd`/result_data/database:/data \
    --volume=`pwd`/result_data/backups:/backups \
    neo4j/neo4j-admin neo4j-admin database dump jejuness:jj_neo4j_docker --to-path=/backups
mv result_data/backups/neo4j.dump result_data/backups/neo4j.CollectingGoldDust.MarkdownTextSplitterAndSentences.dump  
```

Restart the database (out of previous dump)...

```bash
rm -fr result_data/database     # WARNING: this deletes all your databases !
docker run --interactive --tty --rm \
    --volume=`pwd`/result_data/database:/data \
    --volume=`pwd`/result_data/backups:/backups \
    neo4j/neo4j-admin neo4j-admin database load neo4j.CollectingGoldDust.MarkdownTextSplitterAndSentences --from-path=/backups

# Neo4j launching command is identical as the one done above
docker run --rm --detach --name jj_neo4j_db \
    --publish=7474:7474 --publish=7687:7687 \
    --env NEO4J_AUTH=neo4j/your_password \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -v `pwd`/result_data/database:/data \
    jejuness:jj_neo4j_docker
```

Eventually, extract knowledge graph FILE


WARNING: not tested yet

```bash
docker build -t jejuness:jj_neo4j_to_rdf_ttl https://github.com/EricBoix/jj_neo4j_to_rdf_ttl.git#:DockerContext
docker run --rm \
  --network host \
  -v `pwd`/result_data:/output \
  --env-file .env \
  jejuness:jj_neo4j_to_rdf_ttl \
  neo4j_to_rdf.py /output/graph.ttl
```

## Development

### Testing

Within the above running context (directory and installed virtual environment)

```bash
pip install -r requirements-dev.txt
pytest test_main.py
```

### Updating/overwriting the result_data contents

Once development has improved some resulting converted files the following command will overwrite the reference resulting data

```bash
python main.py --output_directory ../result_data/
```

### Code limitations/errors to be fixed

- Some word get modified during extraction: within `output.md` look for
  - the word `eperience` that was initially properly spelled in the sentence `discussing their experiences and discoveries`.
  - the word `ecitement` that was initially properly spelled in the sentence `excitement calming down`
- Some subchapters (quite a few actually) are erroneous. For example the original text doesn't have chapter named `A CAUSE AND EFFECT CHAIN` or `| |`...
