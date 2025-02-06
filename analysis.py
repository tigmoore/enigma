import numpy as np
from scipy.signal import find_peaks, savgol_filter
from scipy.stats import linregress

class ColorResponseAnalyzer:
    def __init__(self, parameters, responses, baseline=0):
        self.parameters = np.array(parameters)
        self.responses = np.array(responses)
        self.baseline = baseline
        self.peaks = []
        self.troughs = []
        self._processed = False
        
    def process(self, peak_prominence=0.03, deriv_threshold=0.15):
        """Main analysis pipeline"""
        self._smooth_responses()
        self._find_peaks(prominence=peak_prominence)
        self._analyze_peaks()
        self._find_invariant_regions(deriv_threshold)
        self._processed = True
        return self
        
    def get_metrics(self):
        if not self._processed:
            raise RuntimeError("Call process() first")
        return {
            'baseline': self.baseline,
            'peaks': self.peaks,
            'troughs': self.troughs,
            'invariance_ranges': self.invariance_ranges,
            'excitatory_sharpness': self._calculate_sharpness(self.peaks),
            'inhibitory_sharpness': self._calculate_sharpness(self.troughs, inhibitory=True)
        }

    def _smooth_responses(self):
        """Prepare data for analysis"""
        self.smoothed = savgol_filter(self.responses, 10, 2) # smoothing window 10 points and polynomial order 2
        self.derivative = np.gradient(self.smoothed, self.parameters)
        
    # def _find_peaks(self, prominence):
    #     """Detect multiple response peaks"""
    #     peaks, props = find_peaks(self.smoothed, 
    #                             prominence=prominence, 
    #                             height=1.2)
    #     self.peak_indices = peaks
    #     self.peak_properties = props
        
    def _find_peaks(self, prominence):
        """Detect both excitatory and inhibitory responses relative to baseline"""
        # For excitatory peaks (above baseline)
        peaks, props = find_peaks(self.smoothed - self.baseline, 
                                prominence=prominence,
                                height=0)  # Must be above baseline
        
        # For inhibitory peaks (below baseline)
        # Invert the signal relative to baseline to find significant drops
        inhibitory_peaks, inhib_props = find_peaks(-(self.smoothed - self.baseline),
                                                prominence=prominence,
                                                height=0)  # Must be below baseline
        
        self.peak_indices = peaks
        self.trough_indices = inhibitory_peaks
        self.peak_properties = props
        self.trough_properties = inhib_props

    def _analyze_peaks(self):
        """Characterize each detected peak/trough"""
        self.peaks = []  # Excitatory peaks
        self.troughs = []  # Inhibitory peaks
        
        # Analyze excitatory peaks
        for idx in self.peak_indices:
            response = self.smoothed[idx]
            peak_val = response - self.baseline
            half_max = peak_val * 0.5  # Half max relative to baseline
            
            # Find FWHM boundaries relative to baseline
            left = np.where(self.smoothed[:idx] - self.baseline < half_max)[0]
            right = np.where(self.smoothed[idx:] - self.baseline < half_max)[0]
            
            start = self.parameters[left[-1]] if left.size > 0 else self.parameters[0]
            end = self.parameters[right[0]+idx] if right.size > 0 else self.parameters[-1]
            
            self.peaks.append({
                'center': self.parameters[idx],
                'range': (start, end),
                'height': response,
                'prominence': self.peak_properties['prominences'][list(self.peak_indices).index(idx)]
            })
    
        # Analyze inhibitory peaks (troughs)
        for idx in self.trough_indices:
            response = self.smoothed[idx]
            trough_val = self.baseline - response  # Magnitude of inhibition
            half_max = trough_val * 0.5  # Half max inhibition
            
            # Find FWHM boundaries for inhibition
            left = np.where(self.baseline - self.smoothed[:idx] < half_max)[0]
            right = np.where(self.baseline - self.smoothed[idx:] < half_max)[0]
            
            start = self.parameters[left[-1]] if left.size > 0 else self.parameters[0]
            end = self.parameters[right[0]+idx] if right.size > 0 else self.parameters[-1]
            
            self.troughs.append({
                'center': self.parameters[idx],
                'range': (start, end),
                'depth': response,  # Actual response value
                'prominence': self.trough_properties['prominences'][list(self.trough_indices).index(idx)]
            })
        
    def _find_invariant_regions(self, threshold):
        """Identify stable regions based solely on derivative"""
        norm_deriv = self.derivative / np.max(np.abs(self.derivative))
        stable_mask = np.abs(norm_deriv) < threshold
        
        changes = np.diff(stable_mask.astype(int))
        starts = np.where(changes == 1)[0] + 1
        ends = np.where(changes == -1)[0]
        
        if stable_mask[0]:
            starts = np.insert(starts, 0, 0)
        if stable_mask[-1]:
            ends = np.append(ends, len(self.parameters)-1)
        
        # Just filter for minimum width
        min_width = 3
        self.invariance_ranges = [(self.parameters[s], self.parameters[e]) 
                                for s, e in zip(starts, ends) 
                                if e - s >= min_width]


    def _calculate_sharpness(self, features, inhibitory=False):
        """Calculate sharpness for peaks or troughs"""
        if not features:  # If list is empty
            return None
        value_key = 'depth' if inhibitory else 'height'
        return np.mean([p['prominence']/abs(p[value_key] - self.baseline) for p in features])
