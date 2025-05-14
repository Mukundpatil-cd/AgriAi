import os
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from PIL import Image

# Image path
DATA_DIR = 'D:/AgriAI/backend/data/plantvillage'


# Image preprocessing transforms
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),  # Converts to [0, 1] range
    transforms.Normalize(mean=[0.485, 0.456, 0.406],  # ImageNet normalization
                         std=[0.229, 0.224, 0.225])
])

# PyTorch dataset
dataset = datasets.ImageFolder(DATA_DIR, transform=transform)

# Print class names
print("Classes:", dataset.classes)

# DataLoader for checking
loader = DataLoader(dataset, batch_size=32, shuffle=True)

# Sanity check
images, labels = next(iter(loader))
print(f"Batch shape: {images.shape}")
print(f"Labels: {labels[:10]}")
