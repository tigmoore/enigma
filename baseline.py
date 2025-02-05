import numpy as np
from stimuli import ColorStimulusGenerator

class BaselineEstimator:
    def __init__(self, model_predictor):
        self.predictor = model_predictor
        self.stim_gen = ColorStimulusGenerator()
        
    def estimate_baseline(self, neuron_idx, n_samples=100):
        """Estimate baseline firing rate using control stimuli"""
        # Generate neutral gray stimuli with random luminance variations
        baselines = []
        for _ in range(n_samples):
            # Random luminance in [0.4, 0.6] range
            lum = np.random.uniform(0.4, 0.6)
            neutral_img = self.stim_gen.generate_solid_color((0, 0, lum))  # HSV (hue=0, saturation=0)
            baselines.append(self.predictor.predict_response(neutral_img, neuron_idx))
            
        return np.percentile(baselines, 10)  # Use 10th percentile 