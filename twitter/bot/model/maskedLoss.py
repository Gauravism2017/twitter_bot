import torch
from torch.jit import script, trace
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
from bot.model.config import *

def maskNLLLoss(inp, target, mask):
    #print("inp {} \n target : {} \n mask {}".format(inp, target.view(-1, 1), mask))
    nTotal = mask.sum()
    crossEntropy = -torch.log(torch.gather(inp, 1, target.view(-1, 1)).squeeze(1))
    loss = crossEntropy.masked_select(mask).mean()
    loss = loss.to(device)
    return loss, nTotal.item()
