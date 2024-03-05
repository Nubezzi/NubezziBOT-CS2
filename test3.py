import torch
from ultralytics import YOLO

print(torch.cuda.is_available())

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')

model = YOLO('best.pt').to(device)