# Neural Color Tuning Analysis

A Python toolkit for analyzing color selectivity and invariance in neural responses from a digital twin of macaque V4 neurons. This project provides tools to characterize how individual neurons respond to color variations in visual stimuli.

## Project Overview

This toolkit analyzes neural responses from a pre-trained CNN model that simulates V4 neural responses to colored images. It focuses on:
- Detecting and characterizing color-selective responses (both excitatory and inhibitory)
- Identifying regions of invariance to color changes

This is done by analysing the changes that arise in a specific neurons response, given different input images that are identical, other than changing hues over the array of the color spectrum. We extract the neural tuning curves for individual neurons over 50 varying hues of color. 

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


## Installation
1. clone the repo
```bash
git clone https://github.com/tigmoore/enigma.git
cd engima
```
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```
3. If not done already, clone and install the repo needed to use the in-silico model
```
git clone -b interview https://github.com/KonstantinWilleke/nnvision.git
pip install -e ./nnvision
```
## Usage

[demo.ipynb](demo.ipynb): Step-by-step tutorial of the analysis pipeline as well as answers to relevant questions
### Quick Start
```python
import os
import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import nnvision
from stimuli import ColorStimulusGenerator
from model import ResponsePredictor
from analysis import ColorResponseAnalyzer
from baseline import BaselineEstimator
from report import ColorTuningReport
from visualize import plot_tuning_with_spectrum, plot_derivative_analysis

# load the model
from nnvision.models.trained_models.v4_task_driven_color import ensemble_model as model

# Specify which neuron within range(394) from the model to analyse 
neuron_idx = 27

# Initialize model and generate color responses
response_predictor = ResponsePredictor(model)
stimulus_generator = ColorStimulusGenerator()
hues = np.linspace(0, 1, 50)
responses = [response_predictor.predict_response(
    stimulus_generator.generate_solid_color((h, 1.0, 0.5)), 
    neuron_idx) for h in hues]

# Analyze color tuning
baseline = BaselineEstimator(response_predictor).estimate_baseline(neuron_idx)
analyzer = ColorResponseAnalyzer(hues, responses, baseline)
analyzer.process()

# Generate visualizations and report, can save or not
plot_tuning_with_spectrum(analyzer, neuron_idx, params_name='Color', save=True)
plot_derivative_analysis(analyzer, neuron_idx, params_name='Color', save=True)
report = ColorTuningReport(analyzer, neuron_idx)
report.save_report(f'reports/neuron_{neuron_idx}_report.txt')
```

## Method Overview

This toolkit implements a systematic approach to analyze color tuning properties of simulated V4 neurons using a digital twin model. The analysis pipeline consists of several key stages:

### 1. Stimulus Generation and Response Collection
- **Color Stimulus Generation**
  - Systematically samples hue values across the color spectrum (0 to 1)
  - Generates solid color images with fixed saturation (1.0) and value (0.5)
  - Uses HSV color space for intuitive color manipulation

- **Neural Response Prediction**
  - Utilizes a pre-trained CNN model that simulates V4 neural responses
  - Predicts spike counts for each color stimulus
  - Processes images of size (1, 3, 100, 100)

### 2. Baseline Estimation
- Estimates baseline firing rate for each neuron using neutral input
- Provides reference point for detecting excitatory and inhibitory responses

### 3. Signal Processing
- **Smoothing**: Applies Savitzky-Golay filtering to raw neural responses
  - Window size: 10 points
  - Polynomial order: 2
  - Purpose: Reduces noise while preserving response shape
- **Derivative Calculation**: Computes gradient to identify rate of neuron response change

### 4. Peak Detection for Selectivity
- **Excitatory Responses**
  - Identifies peaks above baseline
  - Uses prominence-based detection to find significant responses
  - Calculates Full Width at Half Maximum (FWHM) for selectivity range
  - Characterizes each peak by:
    - Center (hue value)
    - Response range
    - Peak height
    - Prominence

- **Inhibitory Responses**
  - Detects significant drops below baseline
  - Inverts signal relative to baseline for trough detection
  - Calculates inhibitory ranges using FWHM
  - Characterizes each trough by:
    - Center (hue value)
    - Response range
    - Trough depth
    - Prominence

### 5. Invariance Detection
- Normalizes response derivative by maximum rate of change
- Identifies regions where normalized derivative is below threshold
- Requires minimum width (3 points) for stable regions
- Characterizes regions where neural response remains constant despite color changes

### 4. Tuning Metrics
- **Sharpness Calculation**
  - For excitatory peaks: prominence/height ratio
  - For inhibitory troughs: prominence/depth ratio
  - Higher values indicate more selective color tuning
  - Separate metrics for excitatory and inhibitory responses

### 5. Key Parameters
- `peak_prominence`: Controls sensitivity of peak/trough detection (default: 0.03)
- `deriv_threshold`: Determines invariance region detection (default: 0.15)
- Both parameters can be adjusted based on signal-to-noise ratio and desired sensitivity

### Visualization
The analysis provides two main visualization types:
1. **Tuning Curve Plot**
   - Raw responses
   - Smoothed response curve
   - Color spectrum background
   - Highlighted selective and invariant regions
   - Peak and trough annotations
![Tuning Curve Example](figures/tuning.png)
2. **Derivative Analysis Plot**
   - Response derivative
   - Threshold regions
   - Invariance indicators
   - Peak/trough markers
![Dervitave Curve Example](figures/derivative.png)

## To Do
- Summary metrics over all neurons to understand population responses 
  - Plot frequency of neurons with large invariance
  - Plot frequency of neurons with very prominent peaks 
