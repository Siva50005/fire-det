from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader 
from torchvision import transforms as T, datasets  
import torch.nn.functional as F 
import uvicorn
from fastapi.responses import JSONResponse
import torch
from PIL import Image as Im
from torchvision.models import squeezenet1_0
from torch import nn
from fastapi.middleware.cors import CORSMiddleware

device = torch.device("cpu" if torch.cuda.is_available() else "cpu") 

# make realtime predictions 
model = squeezenet1_0(pretrained=True) #load pretrained model 
model.classifier[1] = nn.Conv2d(512, 2, kernel_size=(1, 1), stride=(1, 1))
model.load_state_dict(torch.load('fire_squeeze_net.pt')) # load the model
model.to(device)


class_map = [ 
    'fire',
    'no_fire'
]

app = FastAPI()

origins = [
    'http://localhost:8000',
    'http://localhost:3000',
    'http://localhost',
    'http://0.0.0.0:8000'


]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return "Hello World"

@app.post("/predict")
def predict(file: UploadFile):

    INPUT_DIM = 224 
    preprocess = T.Compose([
            T.Resize(INPUT_DIM ),
            T.ToTensor(),
            T.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )])


    im = Im.open(file.file)
    im_preprocessed = preprocess(im) 
    batch_img_tensor = torch.unsqueeze(im_preprocessed, 0)
    output = model(batch_img_tensor) 
    confidence = F.softmax(output, dim=1)[0] * 100 
    _, indices = torch.sort(output, descending=True) 
    return [(class_map[idx], confidence[idx].item()) for idx in indices[0][:1]]


@app.exception_handler(Exception)
async def unicorn_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Server Error"},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",port=8000)