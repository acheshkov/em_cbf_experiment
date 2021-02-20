# Introduction

This repository contains source code to run train/evaluation pipeline for LM/EM problem. 


# How to run

A pipilene requires the following inputs to start:

* ~~Path to CSV with ranges~~
* Path to a CSV file with calculated vectors for EMOs
* Path to a CSV file of Synthetic Dasaset
* Path to a folder where Java Files from Synthetic Dataset are located
* Path to JAR implementing SEMI algorithm


| filename |  range   | vector_str     |
|:---------|:---------|:---------------|
| file_1   | [40, 59] | -0.1 0.3 -0.9  |
| file_1   | [40, 59] | -0.1 0.3 -0.9  |
| file_2   | [40, 59] | -0.1 0.3 -0.9  |


| output_filename | insertion_start | insertion_end  | target_method | target_method_start_line | project_id |
|:----------------|:----------------|:---------------|:--------------|:-------------------------|:-----------|
| file_1   | [40, 59] | -0.1 0.3 -0.9  | file_1   | [40, 59] | -0.1 0.3 -0.9  |




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
