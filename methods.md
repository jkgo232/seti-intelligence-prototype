## Methods



## Overview



The goal is to build a toy-model that takes raw telescope data and converts it into reproducible, multi-modal datasets and analyzes these using a combination of classical signal processing, machine learning, and large language models (LLMs).

--



## Data Sources



The data source used for the development of this project is publicly available radio telescope data from the \*\*Breakthrough Listen Open Data Archive\*\*, collected with the Green Bank Telescope (GBT).



Raw data files are not included in this repository due to size constraints. Instructions for obtaining the data are provided below.



## Data Access



Example datasets may be downloaded from the Breakthrough Listen archive: https://breakthroughinitiatives.org/opendatasearch



After download, raw HDF5 files should be placed in: data/raw/



--



## Preprocessing and RFI Mitigation



Raw spectrogram data are minimally preprocessed to reduce artifacts and common sources of terrestrial radio-frequency interference (RFI).



Preprocessing steps include:



1. Data loading

- HDF5 files are loaded using blimpy.

-  Spectrograms are extracted as 2D time–frequency arrays.



2. Baseline subtraction

-  The median value is subtracted along the time axis to suppress varying backgrounds.



3. Normalization

-  Spectrograms are normalized using median and standard deviation for downstream ML training.



4. RFI masking

-  Frequency channels associated with known RFI bands are masked. (This is currently done minimally and needs to be edited by hand)



The result of this stage is a cleaned, normalized spectrogram ready for tiling and feature extraction.



--



## Spectrogram Tiling and Dataset Construction



To create CNN inputs, preprocessed spectrograms are divided into fixed-size tiles.

-Tile size: 128 × 128 (time × frequency)
-Overlap: default 50% - can be changed
-Tiles with negligible variance or power are discarded to exclude masked regions

Each tile is saved as a NumPy array and accompanied by metadata.

This tiling process produces a dataset of spectrogram tiles/images suitable for CNN training and scoring.

--



## Feature Extraction

In addition to image-based representations, a set of features is saved for each tile. 

Extracted features include:

- Mean normalized power
- Standard deviation 
- Maximum normalized power 
- Kurtosis 
- Spectral entropy

All extracted features are stored in \data\features.npy.



---



## Machine Learning Models

## CNN Embedding Model


A small convolutional neural network is trained to map tiles into a low-dimensional embedding space.

These embeddings are used for visualization, clustering, and signal detection.

--



## Anomaly Detection

Anomaly detection is performed using unsupervised methods.

Implemented approaches include:

-Autoencoder reconstruction error
-Distance-based outlier detection in embedding space
-Feature-based anomaly scoring



The outputs of these methods are combined into a single anomaly score used to rank candidate signals for further inspection.



---



## Synthetic Signal Injection



To evaluate the model sensitivity and validate the pipeline, synthetic signals are injected into a small fraction background data tiles.



Injected signals vary in:

-Signal-to-noise ratio
-Frequency drift rate
-Duration
-Bandwidth


--



## Large Language Models as Reasoning Layers



Large Language Models (LLMs) are evaluated as reasoning layers.



LLMs are given structured textual summaries of signal properties derived from the feature extraction stage. 
For each candidate signal, an LLM is prompted to:

-Assess consistency with known RFI or astrophysical phenomena
-Evaluate alignment with common technosignature heuristics (needs to be specified in script)
-Provide an explanation of its reasoning



Both commercial and open-source LLMs are evaluated for:

-Consistency
-Agreement with heuristic expectations
-Completeness of explanations



---



## Evaluation and Limitations



This is, again, a rough toy-model that is in dire need of optimization at every step. 



---



## Future Work



In addition to optimizing the current pipeline, other extensions include:

-Compatibility with more LLMs
-LLM Fine-Tuning
-Application to interferometric datasets (e.g., ATA, VLA, MeerKAT)
-Real-time inference optimization (e.g., TensorRT)



---









