# Extracting some knowledge graph out of Collecting Gold Dust book<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [Running the converter](#running-the-converter)
- [Running the PDF conversion with docker](#running-the-pdf-conversion-with-docker)
- [Running the full data workflow with jejune\_cli](#running-the-full-data-workflow-with-jejune_cli)
- [Development](#development)

## Introduction

This directory holds a [copy of the pdf version of Sayadaw U Tejaniya's book
COLLECTING GOLD DUST Nurturing the Dhamma in Daily Living](./original_data/2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1.pdf) as offered e.g. by [this Scribd link](https://www.scribd.com/document/716383730/Collecting-Gold-Dust-Web-Book-1).

![The main connected component of some extracted knowledge graph (as visualized with neo4j)](./Doc/main_connected_component_of_knowledge_graph_neo4j_visualization.png)

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
docker build -t jejuneness:doc_Collecting_Gold_Dust https://github.com/EricBoix/jj_doc_Collecting_Gold_Dust.git#:DockerContext
docker run --rm jejuneness:doc_Collecting_Gold_Dust --help
```

Extracting the result out of the container requires local filesystem mount

```bash
docker run --rm  -v `pwd`/junk:/output jejuneness:doc_Collecting_Gold_Dust --output_directory /output
```

## Running the full data workflow with jejune_cli

Install and configure [`jejune_cli`](https://github.com/EricBoix/jejune_cli), then run `jejune doctor` to verify the configuration. This boils down to

```bash
uv tool install git+https://github.com/EricBoix/jejune_cli
jejune configuration init     
# Proceed with the configuration of the files located in .jejune/ sub-directory.
# Assert the configuration is sound with
jejune doctor
```

Define a convenience variable for the results directory:

```bash
export RESULTS_DIR=`pwd`/result_data
```

Run the converter to extract a markdown out of the original PDF :

```bash
jejune convert build
jejune convert run --output-dir $RESULTS_DIR
```

Run the (Knowledge Graph) extraction (starting a neo4j database being prerequisite)

```bash
jejune neo4j delete $RESULTS_DIR    # Avoid collision with previous/other run
jejune neo4j stats --assert 0/0     # Just making sure deletion was effective
jejune neo4j start $RESULTS_DIR
jejune graph extract $RESULTS_DIR \
  --load_markdown_document \
    2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1_-_local_converter.md \
  --load_json_document \
    2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1_-_Sentences_as_LangChain_Document.json
jejune neo4j stats --assert 3279/7726
```

Optional: dump the database content for later usage (and restore it to assert dump integrity/validity)

```bash
jejune neo4j stop
jejune neo4j dump $RESULTS_DIR neo4j.CollectingGoldDust.MarkdownTextSplitterAndSentences.dump
# Restore the database out of the dump (just to make sure)
# WARNING: restoring DELETEs the existing database
jejune neo4j restore $RESULTS_DIR neo4j.CollectingGoldDust.MarkdownTextSplitterAndSentences.dump
jejune neo4j start $RESULTS_DIR
jejune neo4j stats --assert 3279/7726
```

Extract knowledge graph in [Turtle](https://en.wikipedia.org/wiki/Turtle_(syntax)) format

```bash
jejune neo4j dump-turtle $RESULTS_DIR CollectingGoldDust.MarkdownTextSplitterAndSentences.ttl
jejune neo4j stop
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
