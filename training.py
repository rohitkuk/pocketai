
__all__ = ['accuracy', 'report', 'Dataset', 'fit', 'get_dls']

# %% ../nbs/04_minibatch_training.ipynb 1
import pickle,gzip,math,os,time,shutil,torch,matplotlib as mpl,numpy as np,matplotlib.pyplot as plt
from pathlib import Path
from torch import tensor,nn
import torch.nn.functional as F

# %% ../nbs/04_minibatch_training.ipynb 36
def accuracy(out, yb): return (out.argmax(dim=1)==yb).float().mean()

# %% ../nbs/04_minibatch_training.ipynb 39
def report(loss, preds, yb): print(f'{loss:.2f}, {accuracy(preds, yb):.2f}')

# %% ../nbs/04_minibatch_training.ipynb 89
class Dataset():
    def __init__(self, x, y): self.x,self.y = x,y
    def __len__(self): return len(self.x)
    def __getitem__(self, i): return self.x[i],self.y[i]

# %% ../nbs/04_minibatch_training.ipynb 133
from torch.utils.data import DataLoader, SequentialSampler, RandomSampler, BatchSampler

# %% ../nbs/04_minibatch_training.ipynb 149
def fit(epochs, model, loss_func, opt, train_dl, valid_dl):
    for epoch in range(epochs):
        model.train()
        for xb,yb in train_dl:
            loss = loss_func(model(xb), yb)
            loss.backward()
            opt.step()
            opt.zero_grad()

        model.eval()
        with torch.no_grad():
            tot_loss,tot_acc,count = 0.,0.,0
            for xb,yb in valid_dl:
                pred = model(xb)
                n = len(xb)
                count += n
                tot_loss += loss_func(pred,yb).item()*n
                tot_acc  += accuracy (pred,yb).item()*n
        print(epoch, tot_loss/count, tot_acc/count)
    return tot_loss/count, tot_acc/count

# %% ../nbs/04_minibatch_training.ipynb 150
def get_dls(train_ds, valid_ds, bs, **kwargs):
    return (DataLoader(train_ds, batch_size=bs, shuffle=True, **kwargs),
            DataLoader(valid_ds, batch_size=bs*2, **kwargs))
