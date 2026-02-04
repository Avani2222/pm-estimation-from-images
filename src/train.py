import torch
import torch.nn as nn
import torch.optim as optim
from src.dataset import get_loader
from src.model import get_model
from torchvision import transforms

def train_model(df, img_dir, model_name, model_path, device, num_epochs=10, batch_size=32):
    # Transform
    img_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

    # DataLoader
    train_size = int(0.8 * len(df))
    test_size = len(df) - train_size
    from torch.utils.data import random_split
    from src.dataset import AirQualityDataset

    full_dataset = AirQualityDataset(df, img_dir, transform=img_transforms)
    train_dataset, test_dataset = random_split(full_dataset, [train_size, test_size])

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    # Model
    model = get_model(model_name).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    # Training Loop
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            preds = model(imgs)
            loss = criterion(preds, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"[{model_name}] Epoch {epoch+1}/{num_epochs}, Train Loss: {total_loss/len(train_loader):.4f}")

    # Evaluation
    model.eval()
    test_loss = 0
    with torch.no_grad():
        for imgs, labels in test_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            preds = model(imgs)
            loss = criterion(preds, labels)
            test_loss += loss.item()
    print(f"[{model_name}] Test MSE: {test_loss/len(test_loader):.4f}")

    # Save model
    torch.save(model.state_dict(), model_path)