# Introduction

This repository contains source code to compare the following LM/EM algorithms:

 - CBF / code2vec / many projects
 - CBF / code2vec / single projects
 - SEMI [ref]

We compare algorithms using LM/EM benchmark dataset "Synthetic Dataset" [ref].

# Prelimenaries

To start a comparison pipeline, we need to provide the information described below. This information is stores in a `config.ini` file (see Config sections). Before start a pipeline script reads the `config.ini` file. 

### Synthetic dataset location

* Path to an *output* folder where Java Files are located
* Path to a CSV file describing a dataset. 

Synthetic dataset CSV has the following columns. More details here [ref].
  
| output_filename | insertion_start | insertion_end  | target_method | target_method_start_line | project_id       |
|:----------------|----------------:|---------------:|:--------------|-------------------------:|:-----------------|
| file_1          | 40              | 59             | getItem       | 34                       | apache/netbeans  |
| file_2          | 250             | 255            | send          | 234                      | apache/netbeans  |



### Calculated EMO's vectors for CBD/code2vec models

* Path to a CSV file with calculated vectors for EMOs. 

Each row in this table provides vector representation (`vector_str` column) for EMO (`range` column). The `vector_str` column stores vector as a space-separated string of its components. The column `filename` is a link to column `output_filename` of Synthetic Dataset.

| filename | vector_str     |
|:---------|:---------------|
| file_1   | -0.1 0.3 -0.9  |
| file_1   | -0.3 0.1 0.8   |
| file_2   | -0.1 0.3 -0.9  |



### SEMI recommendations

* Path to CSV file with precalculated SEMI recommendations. If file does not exist the it will be calculated from scratch and written on the disk to current folder. 

Each row in this table stores EM recommendations (`semi_recommendations` column). Recommendations stores in a list of line ranges and corresponding scores. The higher score the higher recommendation's rank. The column `filename` links this table with Synthetic Dataset.

| filename |   semi_recommendations                 |
|:---------|:---------------------------------------|
| file_1   | [([66, 91], 466.0), ([66, 80], 342.0)] | 




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


# Config
to describe object fields