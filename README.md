# Introduction

This repository contains source code to run train/evaluation pipeline for LM/EM problem. 


# How to run

A pipilene requires the following inputs to start:

* Path to CSV with ranges
* Path to CSV with calculated vectors for EMOs
* Path to CSV of Synthetic Dasaset
* Path to folder where Java Files from Synthetic Dataset are located
* Path to JAR implementing SEMI algorithm

TODO: explain more

```
$ docker build -t datascience-notebook-java:latest .
$ docker run datascience-notebook-java
```

# Build Docker Image

```
$ docker build -t datascience-notebook-java:latest .
```

# To run tests

```
python3 -m unittest discover -s tests
```
