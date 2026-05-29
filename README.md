# Development directory for my thesis

## Introduction

>[!WARNING]
> This repository is the main development repository for my engineering thesis.
> Please note that the project is currently a proof of concept, not a fully functional production-ready tool.

### Topic of thesis

*Machine learning in road traffic volume measurement. Design and implementation of a tool compliant with the guidelines of the Minister of Infrastructure.*

### Main goal of the thesis

The main goal of the thesis is to implement a proof-of-concept tool for automatic analysis of traffic camera footage and to generate results that can support road traffic volume measurement in a form aligned with Polish legal and technical guidelines.

The project focuses on using computer vision models to detect, track and classify road traffic participants visible in video recordings.

## System concept

The system is designed as a modular processing pipeline instead of a single large model responsible for the whole task. This approach is intended to improve control over each processing stage and reduce unnecessary hardware usage.

The project is divided into three main modules:

1. **Object detection module**

   The detection module is responsible for locating road traffic participants in individual video frames. It detects objects such as pedestrians, bicycles, motorcycles, passenger cars, buses and trucks.

2. **Object tracking module**

   The tracking module is responsible for assigning consistent identifiers to detected objects across consecutive video frames. This step is necessary to avoid counting the same traffic participant multiple times.

3. **Object categorisation module**

   The categorisation module is responsible for assigning detected and tracked objects to traffic-related categories required for further analysis and reporting.

Dividing the system into separate modules makes it possible to test and optimise each stage independently. It also allows the project to use smaller specialised models instead of relying on one computationally expensive end-to-end solution.

## Current stage of development

The current stage of the project focuses on the first module: object detection.

Before integrating detection with tracking and categorisation, selected object detection models need to be benchmarked and compared. The purpose of this stage is to determine which models are the most suitable candidates for road traffic analysis.

The benchmark currently focuses on:

- loading selected object detection models,
- checking whether the models can detect traffic-related object classes,
- unifying detection outputs from different model families,
- preparing a common format for further comparison,
- preparing the basis for evaluation against reference data.

## Model selection

The benchmark includes models available through Torchvision and HuggingFace Transformers. The initial group of analysed models includes architectures such as:

- Faster R-CNN,
- RetinaNet,
- FCOS,
- SSD and SSDLite,
- DETR,
- RT-DETR.

The models are considered mainly in terms of their usefulness as the first stage of the traffic analysis pipeline. The target comparison criteria include:

- detection quality for road traffic participants,
- inference time,
- hardware requirements,
- availability of pretrained weights,
- licence and possible usage limitations,
- ease of integration with tracking and categorisation modules.

The final model selection should not be based only on theoretical average precision reported by model authors. The preferred model should provide a reasonable balance between detection quality and computational cost in the context of traffic camera footage.

## Repository structure

```text
.
├── benchmarks/
│   └── detection_models_benchmark.ipynb
├── video_cocanternation.py
└── README.md
```

### `benchmarks/detection_models_benchmark.ipynb`

Notebook used for the initial technical benchmark of object detection models. It contains the list of analysed models, model loading logic, class filtering logic and early steps toward preparing reference data for evaluation.

### `video_cocanternation.py`

Helper script for concatenating selected video files into a single input video used during experiments.

## Planned next steps

- complete the object detection benchmark,
- standardise the output format of all tested models,
- compare detections with reference annotations,
- calculate quality metrics such as precision, recall and F1-score,
- measure inference time and estimate computational cost,
- rank models using a multi-criteria scoring method,
- select the preferred detection model for further integration,
- add the tracking module,
- add the categorisation and counting module,
- prepare final reporting format for traffic volume analysis.

## Project status

The project is currently under active development. At this stage, the repository contains the first experiments related to object detection model selection. Tracking, categorisation and final reporting modules are planned as later stages of the thesis implementation.
