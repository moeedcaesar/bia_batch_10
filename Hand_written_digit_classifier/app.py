import streamlit as st
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

st.header("Hand-written Digit Classifier")
st.caption("Upload an image. ")
st.caption("The application will classify the handwritten digits into 0-9")
st.caption("Warning: Do not click Recognize button before uploading image. It will result in error.")

class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)

        self.fc1 = nn.Linear(32*7*7, 512)
        self.fc2 = nn.Linear(512, 10)

    def forward(self, x):
        out = self.conv1(x)
        out = self.relu(out)
        out = self.pool(out)

        out = self.conv2(out)
        out = self.relu(out)
        out = self.pool(out)

        out = out.view(-1, 32*7*7)
        out = self.fc1(out)
        out = self.relu(out)
        out = self.fc2(out)
        return out

loaded_model = CNNModel()
loaded_model.load_state_dict(torch.load('D:/bia_deep_learning/cnn_model.pth'))
loaded_model.eval()

class_name = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((28, 28)),
    transforms.ToTensor(), # converts to [0, 1]
    transforms.Normalize((0.1307,), (0.3081,))
])

# Load Image
@st.cache_data
def load_image(image_file):
    img = Image.open(image_file).convert('L')
    return img

imgpath = st.file_uploader("Choose a file", type=("jpg", "jpeg", "png"))
if imgpath is not None:
    img = load_image(imgpath)
    st.image(img, width=300)

def predict_label(image):
    img_tensor = transform(image).unsqueeze(0) # add batch dimension
    with torch.no_grad():
        outputs = loaded_model(img_tensor)
        _, predicted = torch.max(outputs, 1)
        return class_name[predicted.item()]

if st.button("Recognize"):
    if imgpath is not None:
        predicted_label = predict_label(img)
        st.write(f"The image is predicted to be **{predicted_label}**.")
    else:
        st.warning("Please upload an image first.")