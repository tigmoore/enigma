import textwrap
import os

class ColorTuningReport:
    def __init__(self, analyzer, neuron_idx=None):
        """Initialize report with analyzer results and optional neuron ID"""
        self.metrics = analyzer.get_metrics()
        self.analyzer = analyzer
        self.neuron_idx = neuron_idx

    def save_report(self, filename):
        """Save report to a text file"""
        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)
        report_text = []
        if self.neuron_idx is not None:
            report_text.append(f"Neuron ID: {self.neuron_idx}\n")
        report_text.append(self.generate_report())
        
        with open(filename, 'w') as f:
            f.write('\n'.join(report_text))

    def generate_report(self):
        """Create full analysis report"""
        return self._create_summary_text()

    def _hue_to_color(self, hue):
        """Convert hue value (0-1) to approximate color name"""
        # Define color ranges (these can be adjusted)
        color_ranges = {
            (0, 0.042): "red",
            (0.042, 0.125): "orange",
            (0.125, 0.208): "yellow",
            (0.208, 0.375): "green",
            (0.375, 0.458): "turquoise",
            (0.458, 0.542): "cyan",
            (0.542, 0.625): "light blue",
            (0.625, 0.708): "blue",
            (0.708, 0.792): "purple",
            (0.792, 0.875): "magenta",
            (0.875, 0.958): "pink",
            (0.958, 1.0): "red"
        }
        
        for (start, end), color in color_ranges.items():
            if start <= hue < end:
                return color
        return "red"  # For hue = 1.0

    def _create_summary_text(self):
        """Generate report text for multi-peak results"""
        lines = [
            f"{' COLOR TUNING ANALYSIS:':=^70}",
            f"Baseline firing rate: {self.metrics['baseline']:.2f} spk/100ms",
            f"Detected excitatory peaks: {len(self.metrics['peaks'])}",
            f"Detected inhibitory troughs: {len(self.metrics['troughs'])}",
            ""
        ]
        
        # Excitatory peak details
        if self.metrics['peaks']:
            lines.append("EXCITATORY RESPONSES:")
            for i, peak in enumerate(self.metrics['peaks']):
                start_color = self._hue_to_color(peak['range'][0])
                end_color = self._hue_to_color(peak['range'][1])
                center_color = self._hue_to_color(peak['center'])
                lines += [
                    f"Peak {i+1}:",
                    f"  Center: {peak['center']:.2f} ({center_color})",
                    f"  Selective range: {peak['range'][0]:.2f} - {peak['range'][1]:.2f}",
                    f"  Color range: {start_color} to {end_color}",
                    f"  Peak height: {peak['height']:.2f} spk/100ms",
                    f"  Prominence: {peak['prominence']:.2f} spk/100ms",
                    ""
                ]
            
        # Inhibitory trough details
        if self.metrics['troughs']:
            lines.append("INHIBITORY RESPONSES:")
            for i, trough in enumerate(self.metrics['troughs']):
                start_color = self._hue_to_color(trough['range'][0])
                end_color = self._hue_to_color(trough['range'][1])
                center_color = self._hue_to_color(trough['center'])
                lines += [
                    f"Trough {i+1}:",
                    f"  Center: {trough['center']:.2f} ({center_color})",
                    f"  Selective range: {trough['range'][0]:.2f} - {trough['range'][1]:.2f}",
                    f"  Color range: {start_color} to {end_color}",
                    f"  Trough depth: {trough['depth']:.2f} spk/100ms",
                    f"  Prominence: {trough['prominence']:.2f} spk/100ms",
                    ""
                ]
        
        # Invariance regions with color names
        if self.metrics['invariance_ranges']:
            lines.append("INVARIANT REGIONS:")
            for i, region in enumerate(self.metrics['invariance_ranges']):
                start_color = self._hue_to_color(region[0])
                end_color = self._hue_to_color(region[1])
                lines += [
                    f"Region {i+1}:",
                    f"  Range: {region[0]:.2f} - {region[1]:.2f}",
                    f"  Colors: {start_color} to {end_color}",
                    ""
                ]
            
        lines += [
            f"Total invariance regions: {len(self.metrics['invariance_ranges'])}",
        ]
        
        if self.metrics['excitatory_sharpness'] is not None:
            lines.append(f"Average excitatory sharpness: {self.metrics['excitatory_sharpness']:.2f}")
        if self.metrics['inhibitory_sharpness'] is not None:
            lines.append(f"Average inhibitory sharpness: {self.metrics['inhibitory_sharpness']:.2f}")
            
        return '\n'.join(lines)
 
