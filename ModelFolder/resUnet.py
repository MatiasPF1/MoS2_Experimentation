import torch
import torch.nn as nn


# Built with help of Video: https://www.youtube.com/watch?v=H604sFU_0ME&t=6s
# Minute: 11:40
# Table I – Network Structure of ResUNet Given in the Papper 
# --------------------------------------
# Input: 224×224×3
#
# Encoding:
# L1: Conv1 (3×3/64, s=1) → 224×224×64
#     Conv2 (3×3/64, s=1) → 224×224×64
# L2: Conv3 (3×3/128, s=2) → 112×112×128
#     Conv4 (3×3/128, s=1) → 112×112×128
# L3: Conv5 (3×3/256, s=2) → 56×56×256
#     Conv6 (3×3/256, s=1) → 56×56×256
#
# Bridge:
# L4: Conv7 (3×3/512, s=2) → 28×28×512
#     Conv8 (3×3/512, s=1) → 28×28×512
#
# Decoding:
# L5: Conv9  (3×3/256, s=2) → 56×56×256
#     Conv10 (3×3/256, s=1) → 56×56×256
# L6: Conv11 (3×3/128, s=2) → 112×112×128
#     Conv12 (3×3/128, s=1) → 112×112×128
# L7: Conv13 (3×3/64, s=2) → 224×224×64
#     Conv14 (3×3/64, s=1) → 224×224×64
#
# Output:
# Conv15 (1×1/1, s=1) → 224×224×1





# --------------------------------------
# Batch and Relu In a Single Module
class BatchAndRelu(nn.Module):
    def __init__(self, ConvInput):
        self.bn-nn.BatchNorm2d(ConvInput)
        self.relu=nn.ReLU()

    def forward(self,input):
        x=self.bn(input)
        x=self.relu(x)
        return x

# --------------------------------------
# Residual Block       
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        '''Convolution Layer'''
        self.b1= BatchAndRelu(in_channels)
        self.c1= nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, stride= stride) #Stride can be 1 or 2
        self.b2= BatchAndRelu(out_channels)
        self.c2= nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, stride=1) # This Stride is always 1 

        '''Shortcut Connection'''
        self.s=nn.Conv2d(in_channels, out_channels, kernel_size=1, padding=0, stride=stride) # Adjusting dimensions
    
    def forward(self, input):
        x=self.b1(input)
        x=self.c1(x)
        x=self.b2(x)
        x=self.c2(x)
        skip=self.s(input)
        out=x+skip
        return out


# --------------------------------------
# ResUnet Model
class ResUnet(nn.Module):
    def __init__(self):
        super()._init_()

        '''Encoder L1 - Different from other Layers'''
        #Input: 224x224x3
        self.conv1=nn.Conv2d(3, 64, kernel_size=3, padding=1, stride=1)
        self.bn_relu1=BatchAndRelu(64) #64 channels after conv1
        self.conv1_2=nn.Conv2f(64, 64, kernel_size=3, padding=1, stride=1)
        self.Residual1=nn.Conv2d(3, 64, kernel_size=1, padding=0, stride=1) #Residual
        ''' EnCoder 2 and 3'''

    def forward(self, input):
        '''Encoder L1 Forward'''
        x=self.conv1(input) # 224x224x3 --> 224x224x64
        x=self.bn_relu1(x)
        x=self.conv1_2(x) # 224x224x64 --> 224x224x64
        residual= self.Residual1(input) # 224x224x3 --> 224x224x64
        Skip1 = x + residual  # Addinf Residual, also saving Connection for Decoding 
