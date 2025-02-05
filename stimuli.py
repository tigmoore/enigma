import colorsys
from PIL import Image

class ColorStimulusGenerator:
    def __init__(self, image_size=100):
        self.image_size = image_size
    
    def _hsv_to_rgb(self, hsv_values):
        """Convert HSV values (0-1 range) to RGB tuple (0-255 range)"""
        h, s, v = hsv_values
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r*255), int(g*255), int(b*255))
    
    def generate_solid_color(self, hsv_values):
        """Generate full-field color patch"""
        color = self._hsv_to_rgb(hsv_values)
        return Image.new('RGB', (self.image_size, self.image_size), color)