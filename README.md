# CLL TDA ML Research Public

Public version of a research pipeline combining Topological Data Analysis and Machine Learning for chronic lymphocytic leukemia.

This repository is designed for reproducible demonstrations using public or synthetic data only.

## Scientific objective

Build a dynamic mapping linking biological trajectories to clinical trajectories in chronic lymphocytic leukemia, in order to provide a geometric interpretation of disease heterogeneity.

## Why this project?

Chronic lymphocytic leukemia is clinically heterogeneous. Classical clinical and biological markers do not always fully capture the geometry of patient heterogeneity.

This project explores whether topological signatures extracted from patient-level biological representations can enrich clinical risk stratification.

## Pipeline

The repository follows a 10-step pipeline:

1. project overview and data dictionary;
2. data audit and preprocessing;
3. endpoint definition and cohort selection;
4. classical Machine Learning baselines;
5. survival analysis baseline;
6. geometric patient space with PCA and UMAP;
7. TDA persistence features;
8. hybrid TDA + Machine Learning models;
9. dynamic biological-clinical mapping;
10. interpretability, robustness and final figures.

## Repository structure

```text
configs/        Pipeline configuration
data/           Public or synthetic data folders
docs/           Scientific and methodological documentation
notebooks/      Ordered analysis notebooks
src/            Reusable Python package
scripts/        Utility and pipeline scripts
results/        Generated outputs
tests/          Minimal tests
