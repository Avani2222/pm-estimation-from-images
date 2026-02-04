import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dataset import AirQualityDataset, get_loader
from model import get_model, load_model
from inference import predict_image