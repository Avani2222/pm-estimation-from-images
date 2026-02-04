import torch
import torch.nn as nn
from torchvision import models

def get_model(model_name, num_outputs=7):
    if model_name == "resnet18":
        model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        model.fc = nn.Linear(512, num_outputs)

    elif model_name == "resnet34":
        model = models.resnet34(weights=models.ResNet34_Weights.IMAGENET1K_V1)
        model.fc = nn.Linear(512, num_outputs)

    elif model_name == "mobilenet_v2":
        model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_outputs)

    else:
        raise ValueError(f"Unknown model: {model_name}")

    return model

def load_model(model_name, model_path, device):
    model = get_model(model_name).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model