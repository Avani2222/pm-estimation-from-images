import os
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from torchvision import transforms

class AirQualityDataset(Dataset):
    def __init__(self, df, img_dir, transform=None):
        self.df = df.reset_index(drop=True)
        self.img_dir = img_dir
        self.transform = transform
        self.label_cols = ['AQI','PM2.5','PM10','O3','CO','SO2','NO2']

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        filename = row["Filename"].strip()
        img_path = os.path.join(self.img_dir, filename)

        if not os.path.exists(img_path):
            raise FileNotFoundError(f"File not found: {img_path}")

        img = Image.open(img_path).convert("RGB")
        if self.transform:
            img = self.transform(img)

        labels = torch.tensor(
            row[self.label_cols].astype(float).values,
            dtype=torch.float32
        )

        return img, labels

def get_loader(df, img_dir, batch_size=32, shuffle=False, transform=None):
    dataset = AirQualityDataset(df, img_dir, transform)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)