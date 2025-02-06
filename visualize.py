import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb, LinearSegmentedColormap


def plot_derivative_analysis(analyzer, params_name, threshold=0.1):
    """Plot derivative with threshold regions and invariance analysis"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Calculate normalized derivative and threshold
    max_deriv = np.max(np.abs(analyzer.derivative))
    threshold_value = threshold * max_deriv
    
    # Add threshold bands
    ax.fill_between(analyzer.parameters, 
                   threshold_value, 
                   -threshold_value, 
                   color='lightgrey', 
                   alpha=0.3, 
                   label='Threshold Region')
    
    # Derivative curve
    ax.plot(analyzer.parameters, analyzer.derivative, 
            color='orange', linewidth=2, label='Derivative')
    
    # Add threshold lines
    ax.axhline(threshold_value, color='red', linestyle='--', 
               alpha=0.5, label='Threshold')
    ax.axhline(-threshold_value, color='red', linestyle='--', 
               alpha=0.5)
    
    # Zero line
    ax.axhline(0, color='k', linestyle='-', alpha=0.3, linewidth=0.8)
    
    # Mark peaks 
    y_lim = ax.get_ylim()
    for i, peak in enumerate(analyzer.peaks):
        ax.axvline(peak['center'], color='blue', linestyle=':', 
                  alpha=0.5, label='Peak')
        # Place text inside plot near top
        ax.text(peak['center'], y_lim[1]*0.9,  # Position at 90% of y-axis height
                f'Peak {i+1}',
                rotation=0,
                va='bottom',
                ha='center',
                fontsize=9,
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))  # Add white background
    
    # Mark troughs 
    y_lim = ax.get_ylim()
    for i, peak in enumerate(analyzer.troughs):
        ax.axvline(peak['center'], color='blue', linestyle=':', 
                  alpha=0.5, label='Trough')
        # Place text inside plot near top
        ax.text(peak['center'], y_lim[1]*0.9,  # Position at 90% of y-axis height
                f'Trough {i+1}',
                rotation=0,
                va='bottom',
                ha='center',
                fontsize=9,
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))  # Add white background
 
    # Formatting
    ax.set_xlabel(f'{params_name} Value', fontsize=12)
    ax.set_ylabel('dResponse/dColor', fontsize=12)
    ax.set_title('Derivative Analysis with Threshold Regions', fontsize=14)
    
    # Handle legend duplicates
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), 
             loc='upper right', frameon=True)
    
    plt.tight_layout()
    plt.show()
    return fig


def _plot_invariance_ranges(ax, analyzer):
    """Add invariance regions from derivative analysis"""
    for region in analyzer.invariance_ranges:
        ax.axvspan(*region, color='yellow', alpha=0.3, 
                  label='Invariance Region', zorder=1)



def plot_tuning_with_spectrum(analyzer, params_name='Color'):
    """Create comprehensive plot with color spectrum background"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create color spectrum background
    n_colors = 50
    for i in np.linspace(0, 1, n_colors):
        ax.axvline(i, color=hsv_to_rgb([i, 1, 1]), linewidth=4, alpha=0.15, zorder=0)
    
    # Plot neural responses
    ax.plot(analyzer.parameters, analyzer.responses, 'o',
            color='grey', alpha=0.6, markersize=5, label='Raw Responses', zorder=2)
    ax.plot(analyzer.parameters, analyzer.smoothed,
            color='blue', linewidth=2.5, label='Smoothed', zorder=3)
    
    # Plot baseline with different style
    ax.axhline(analyzer.baseline, color='black', linestyle='--', 
               label='Baseline', linewidth=1.5, zorder=1)
    
    # Add analysis elements
    _plot_selectivity_regions(ax, analyzer)
    _plot_invariance_ranges(ax, analyzer)
    _add_annotations(ax, analyzer)
    
    # Formatting
    ax.set_xlabel(f'{params_name} Value', fontsize=12)
    ax.set_ylabel('Firing Rate (spk/100ms)', fontsize=12)
    ax.set_title(f'Color Tuning Analysis with {params_name} Spectrum', fontsize=14)
    ax.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    plt.show()
    return fig


def _plot_selectivity_regions(ax, analyzer):
    """Add FWHM regions for both excitatory and inhibitory responses"""
    # Excitatory peaks (blue shading)
    for i, peak in enumerate(analyzer.peaks):
        ax.axvspan(*peak['range'], color='blue', alpha=0.2,
                  label=f'Peak {i+1} Selectivity', zorder=1)
        
    # Inhibitory troughs (red shading)
    for i, trough in enumerate(analyzer.troughs):
        ax.axvspan(*trough['range'], color='red', alpha=0.2,
                  label=f'Trough {i+1} Selectivity', zorder=1)

def _add_annotations(ax, analyzer):
    """Add peak/trough markers and text labels"""
    # Annotate excitatory peaks
    for i, peak in enumerate(analyzer.peaks):
        ax.plot(peak['center'], peak['height'], 'o', color='red',
                markersize=8, zorder=4)
        ax.text(peak['center'], peak['height']*.98, f'Peak {i+1}\n({peak["center"]:.2f})',
                ha='center', fontsize=9, color='red')
    
    # Annotate inhibitory troughs
    for i, trough in enumerate(analyzer.troughs):
        ax.plot(trough['center'], trough['depth'], 'o', color='red',
                markersize=8, zorder=4)
        ax.text(trough['center'], trough['depth']*1.01, f'Trough {i+1}\n({trough["center"]:.2f})',
                ha='center', fontsize=9, color='red')
