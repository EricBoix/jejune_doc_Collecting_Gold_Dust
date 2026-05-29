# Extracting the book semantic structure out of Collecting Gold Dust book<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [Running the converter](#running-the-converter)
- [Running with docker](#running-with-docker)
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

## Running with docker

```bash
docker build -tjejuness:doc_Collecting_Gold_Dust https://github.com/EricBoix/jj_doc_Collecting_Gold_Dust.git#:DockerContext
docker run --rm jejuness:doc_Collecting_Gold_Dust --help
```

Extracting the result out of the container required local filesystem mount

```bash
docker run --rm  -v `pwd`/junk:/output jejuness:doc_Collecting_Gold_Dust --output_directory /output 
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
