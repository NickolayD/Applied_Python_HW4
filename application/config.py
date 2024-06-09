import gdown
import os
import torch


class ConvNet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2),
            torch.nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2),
            torch.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2),  
            torch.nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1),
            torch.nn.ReLU()        
        )
        self.classifier = torch.nn.Linear(in_features=128, out_features=15)

    def forward(self, x):
        feature_map = self.net(x)
        feature_vector = feature_map.mean(dim=(2, 3))
        logits = self.classifier(feature_vector)
        return logits
        

# для загрузки pickle-файла с обученной ML моделью
url = 'https://drive.google.com/uc?id=1hdzhVISaI1HURIRGthbEtRTEfdvH-E_E'
filename = 'cnn.pt'
if filename not in os.listdir():
    gdown.download(url, filename, quiet=False)

# Объявление модели и инициализация весов
ckpt = torch.load('cnn.pt', map_location=torch.device('cpu'))
model = ConvNet()
model.load_state_dict(ckpt['model'])

# словарь с лейблами классов
veg_dict = {
    0: "Бобы (Bean)",
    1: "Горькая тыква (Bitter Gourd)",
    2: "Бутылочная тыква (Botter Gourd)",
    3: "Баклажан (Brinjal)",
    4: "Брокколи (Broccoli)",
    5: "Капуста (Cabbage)",
    6: "Стручковый перец (Capsicum)",
    7: "Морковь (Carrot)",
    8: "Цветная капуста (Cauliflower)",
    9: "Огурец (Cucumber)",
    10: "Папайя (Papaya)",
    11: "Картофель (Potato)",
    12: "Тыква (Pumpkin)",
    13: "Редька (Radish)",
    14: "Томат (Tomato)",
}
