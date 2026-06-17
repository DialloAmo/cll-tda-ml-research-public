# Methodology

## Pipeline

1. Data loading
2. Data audit and preprocessing
3. Endpoint definition
4. Classical ML baseline
5. Survival baseline if time-to-event data are available
6. Patient-space geometry with PCA and UMAP
7. Persistent homology and TDA features
8. Hybrid TDA + ML model
9. Evaluation
10. Clinical and biological interpretation

## Evaluation

Depending on the endpoint:

- AUC
- F1-score
- recall
- precision
- ROC curves
- calibration
- C-index
- Brier score
- stratified cross-validation

## Interpretability

- permutation importance
- SHAP values
- risk-group comparison
- PCA / UMAP visualizations
- topological signatures associated with IGHV, TP53, del(17p), Rai or Binet
