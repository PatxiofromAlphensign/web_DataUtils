import numpy as np
import torch
from train import batch_generator
from evaluation import Model

def unsim_vector(x):
    assert len(x.shape) == 2
    y = torch.zeros(x.shape[0], x.shape[1])
    y_prime = []
    for i in range(x.shape[0]-2):
        if i>x.shape[0] -2:
            break
        for k in range(x.shape[1]):
            y[i,k] = (x[i,k]!=x[i+1,k])*1
    dots = []

    for xc,yc in zip(x,y):
       dots.append(torch.dot(xc,yc))

    return torch.Tensor(dots)

def sim_vector(x):
    assert len(x.shape) == 2
    y = torch.zeros(x.shape[0], x.shape[1])
    y_prime = []
    for i in range(x.shape[0]-2):
        if i>x.shape[0] -2:
            break
        for k in range(x.shape[1]):
            y[i,k] = (x[i,k]==x[i+1,k])*1
    dots = []

    for xc,yc in zip(x,y):
       dots.append(torch.dot(xc,yc))

    return torch.Tensor(dots)


x = np.arange(5)
y = np.arange(20)[x.shape[0]:][:x.shape[0]]


#print(sum([x,y[:x.shape[0]]]).argsort()[::-1])

class demoPlay(Model):
    def __init__(self, x, y):

        inputs = torch.Tensor([x,y])
        input_inv = inputs.permute(1,0)

        pad_iinv = torch.ones(inputs.shape[1], input_inv.shape[0])
        pad_i = torch.ones(inputs.shape[1], input_inv.shape[0])
        for i in range(input_inv.shape[0]):
            pad_iinv[i,:input_inv.shape[1]] = input_inv[i]  
        
        pad_i[:inputs.shape[0]] = inputs
            

        padded_scale =(pad_i*pad_iinv)/2 
        #y_inv = sim_vector(y)
        #y = torch.Tensor([y,y_inv])
        
        super(demoPlay, self).__init__(padded_scale.numpy(), input_inv.numpy())
        
    def forward_playful(self, x=None):

        pass




print(demoPlay(x,y))
