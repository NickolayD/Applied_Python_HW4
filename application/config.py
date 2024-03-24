import gdown
import os
import pickle


# для загрузки pickle-файла с обученной ML моделью
url = 'https://drive.google.com/uc?id=15csxuXKm1MCuZUqASTbge1XY-rci3V8X'
filename = 'LinearSVCBest.pkl'
if filename not in os.listdir():
    gdown.download(url, filename, quiet=False)
with open(filename, "rb") as file:
    model = pickle.load(file)

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
