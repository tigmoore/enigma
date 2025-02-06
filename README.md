# Neural Color Tuning Analysis

A Python toolkit for analyzing color selectivity and invariance in neural responses from a digital twin of macaque V4 neurons. This project provides tools to characterize how individual neurons respond to color variations in visual stimuli.

## Project Overview

This toolkit analyzes neural responses from a pre-trained CNN model that simulates V4 neural responses to colored images. It focuses on:
- Detecting and characterizing color-selective responses (both excitatory and inhibitory)
- Identifying regions of invariance to color changes
- Visualizing tuning curves with color spectrum analysis
- Quantifying selectivity through tuning curves

## Features

- **Color Response Analysis**
  - Detection of excitatory peaks and inhibitory troughs
  - Identification of color-invariant regions
  - Calculation of tuning sharpness metrics
  - Smoothing and derivative analysis

- **Visualization Tools**
  - Color tuning curves with spectrum overlay
  - Derivative analysis plots
  - Selective and invariant region highlighting
  - Automated peak and trough annotation

- **Reporting**
  - Detailed analysis reports including:
    - Peak/trough characteristics
    - Color selectivity ranges
    - Invariance regions
    - Response metrics

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```
2. If not done already, clone and install the repo needed to use the in-silico model
```
git clone -b interview https://github.com/KonstantinWilleke/nnvision.git
pip install -e ./nnvision
```
