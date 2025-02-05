import torch
import numpy as np

class ResponsePredictor:
    def __init__(self, model, device=None):
        """
        Initialize predictor with automatic device detection
        :param model: Pre-trained model instance
        :param device: Optional device override (e.g., 'cuda', 'cpu')
        """
        self.device = self._get_device(device)
        self.model = model.eval().to(self.device)
        self.img_mean = 113.5
        self.img_std = 59.58

    def _get_device(self, device_override):
        """Determine best available device"""
        if device_override:
            return torch.device(device_override)
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def _preprocess_image(self, pil_image):
        """Convert PIL image to normalized tensor with device placement"""
        img_array = np.array(pil_image, dtype=np.float32)
        tensor = torch.from_numpy(img_array)
        tensor = (tensor - self.img_mean) / self.img_std
        return tensor.permute(2, 0, 1).unsqueeze(0).to(self.device)

    def predict_response(self, image, neuron_idx, data_key='all_sessions'):
        """
        Get predicted spike count for specified neuron
        :param image: PIL Image object
        :param neuron_idx: Target neuron index
        :param data_key: Model data key (default: 'all_sessions')
        """
        tensor = self._preprocess_image(image)
        with torch.no_grad():
            output = self.model(tensor, data_key=data_key)
        return output[0, neuron_idx].item()