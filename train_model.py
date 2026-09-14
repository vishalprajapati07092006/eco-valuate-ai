import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from torch.utils.data import random_split, DataLoader
import json
import os

def run_training():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🚀 Using Device: {device}")

    dataset_path = "my_dataset"
    save_dir = "models"
    os.makedirs(save_dir, exist_ok=True)

    if not os.path.exists(dataset_path):
        print(f"❌ Error: Folder '{dataset_path}' not found! Place your dataset folder in the project root.")
        return

    data_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    full_dataset = datasets.ImageFolder(dataset_path, transform=data_transform)
    class_names = full_dataset.classes
    num_classes = len(class_names)
    print(f"✅ Discovered {num_classes} classes: {class_names}")

    with open(os.path.join(save_dir, "class_index.json"), "w") as f:
        json.dump({i: cls for i, cls in enumerate(class_names)}, f, indent=4)

    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

    dataloaders = {
        'train': DataLoader(train_dataset, batch_size=16, shuffle=True),
        'val': DataLoader(val_dataset, batch_size=16, shuffle=False)
    }

    model = models.efficientnet_b0(pretrained=True)
    for param in model.parameters():
        param.requires_grad = False

    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier[1].parameters(), lr=0.001)

    epochs = 5
    print("\n⏳ Starting model training...")
    for epoch in range(epochs):
        for phase in ['train', 'val']:
            model.train() if phase == 'train' else model.eval()
            running_loss, running_corrects = 0.0, 0

            for inputs, labels in dataloaders[phase]:
                inputs, labels = inputs.to(device), labels.to(device)
                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            dataset_len = train_size if phase == 'train' else val_size
            epoch_acc = running_corrects.double() / dataset_len
            print(f"Epoch {epoch+1}/{epochs} - [{phase.upper()}] Accuracy: {epoch_acc*100:.2f}%")

    torch.save(model.state_dict(), os.path.join(save_dir, "dynamic_ewaste.pth"))
    print("\n🎉 Model trained successfully and saved to models/dynamic_ewaste.pth!")

if __name__ == "__main__":
    run_training()
    
    
    
    
    
    
    
    