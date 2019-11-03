"""annoying boilerplate to get cycleGAN working
in the context of a Flask app"""

import os, sys
sys.path.append(os.path.join(os.getcwd(), "pytorch-CycleGAN-and-pix2pix"))

import numpy as np
import torch
import torchvision
from data.single_dataset import SingleDataset
from data.base_dataset import get_transform
from models.cycle_gan_model import CycleGANModel
from util.util import tensor2im

from PIL import Image
from argparse import Namespace
from pathlib import Path

model_fp = Path("./dragnet_weights.pth").resolve()
assert model_fp.exists()

opt = Namespace(aspect_ratio=1.0,
                batch_size=1,
                checkpoints_dir='./checkpoints',
                crop_size=256,
                dataroot=".",
                dataset_mode='unaligned',
                direction='AtoB',
                display_id=-1,
                display_winsize=256,
                epoch='latest',
                eval=False,
                gpu_ids=[],
                init_gain=0.02,
                init_type='normal',
                input_nc=3,
                isTrain=False,
                load_iter=0,
                load_size=256,
                max_dataset_size=float("inf"),
                model='cycle_gan',
                n_layers_D=3,
                name='dragnet',
                ndf=64,
                netD='basic',
                netG='resnet_9blocks',
                ngf=64,
                no_dropout=True,
                no_flip=True,
                norm='instance',
                ntest=float("inf"),
                num_test=100,
                num_threads=0,
                output_nc=3,
                phase='test',
                preprocess='no_preprocessing',
                results_dir='./results/',
                serial_batches=True,
                suffix='',
                verbose=False)
model = CycleGANModel(opt).netG_A
model.load_state_dict(torch.load(model_fp))

preprocess = get_transform(opt)

class SingleImageDataset(torch.utils.data.Dataset):

    def __init__(self, *args, **kwargs):
        img = kwargs.pop("img")
        super().__init__(*args, **kwargs)
        img = preprocess(img)
        self.img = img
        
    def __getitem__(self, i):
        return self.img

    def __len__(self):
        return 1

def translate_face_subimage(subimg):
    data_loader = torch.utils.data.DataLoader(
        SingleImageDataset(img=subimg),
        batch_size=1
    )
    for data in data_loader:
        with torch.no_grad():
            pred = model(data)
    pred_arr = tensor2im(pred)
    pred_img = Image.fromarray(pred_arr)
    return pred_img

