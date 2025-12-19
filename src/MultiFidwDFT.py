#!/usr/bin/env python
# coding: utf-8

# In[3]:


import torch
import gpytorch as gpt
import botorch
from botorch.models import SingleTaskMultiFidelityGP, SingleTaskGP
from botorch.models.transforms.input import Normalize
from botorch.models.transforms.outcome import Standardize
from botorch.fit import fit_gpytorch_mll, fit_gpytorch_mll_torch
from torch.optim import Adam
from gpytorch.mlls import ExactMarginalLogLikelihood
import numpy as np
import HeBz

# Use CPU for this example
device = torch.device("cuda")
dtype = torch.float64


# In[4]:


#Load the data from file
V = np.load('HeBz_sector_2475.npy')
x = np.array([])
y = np.array([])
z = np.array([])
data_points = []
Pot = np.array([])
Pot_diff = np.array([])
for array in V:
    x = np.append(x,array[0])
    y = np.append(y,array[1])
    z = np.append(z,array[2])
    data_points.append([array[0],array[1],array[2],1.0])
    Pot = np.append(Pot,array[3])
V2 = np.load('new_pts_70.npy')
for array in V2:
    x = np.append(x,array[0])
    y = np.append(y,array[1])
    z = np.append(z,array[2])
    data_points.append([array[0],array[1],array[2],1.0])
    Pot = np.append(Pot,array[3])
data_points = np.array(data_points)
noise = 1e-6*np.ones_like(Pot)

# In[24]:


# -----------------------------
# 1. Generate Source Task Data
# -----------------------------
DFTdata0 = np.load("pbe0_113850_CP_D4_processed.npy")
ind = np.where(np.isclose(DFTdata0[:,2],0.09459459))
refdata = DFTdata0[ind]
refdata[:,2] = -1*refdata[:,2]
DFTdata = np.concatenate((DFTdata0,refdata))
ind = np.argsort(DFTdata[:,2], kind='stable')
DFTdatazsrt = DFTdata[ind]
ind = np.argsort(DFTdatazsrt[:,1], kind='stable')
DFTdatayzsrt = DFTdatazsrt[ind]
DFTdataxrem = DFTdatayzsrt[::8]
ind = np.argsort(DFTdataxrem[:,0], kind='stable')
DFTdataxremzsrt = DFTdataxrem[ind]
#DFTdata2 = np.load("pbe0_corr_sutirtha_CP_D4_full_processed.npy")
#DFTdatanew = np.concatenate((DFTdata2[:,0],DFTdata2[:,1],DFTdata2[:,2]),)
DFTdatazxrem = DFTdataxremzsrt
DFTdata2 = np.load("pbe0_corr_sutirtha_CP_D4_full_processed.npy")
DFTtotal = np.concatenate((DFTdatazxrem[:,0:3],DFTdata2[:,0:3]))
data_source = [[x, y, z, w] for x, y, z, w in zip(DFTtotal[:,0],DFTtotal[:,1],DFTtotal[:,2],np.zeros(len(DFTtotal)))]
m_source = np.concatenate((DFTdatazxrem[:,-1],DFTdata2[:,-1]))
#DFTtotal = np.concatenate((DFTdatazxrem[:,0:4],DFTdata2[:,0:4]))
#np.concatenate(DFTdatazxrem,[[
#print(np.unique(DFTdataxremzsrt[:,2]))
#print(np.unique(DFTdatazxrem[:,2]))
#data_source = [[x, y, z, w] for x, y, z, w in zip(DFTdatazxrem[:,0],DFTdatazxrem[:,1],DFTdatazxrem[:,2],np.zeros(len(DFTdatazxrem)))]
#m_source = DFTdatazxrem[:,-1]
noise_source = 1e-6*np.ones_like(m_source) 
# In[25]:


train_X = np.concatenate((data_points,data_source))
train_Y = np.concatenate((Pot,m_source))
train_Y = train_Y.reshape(-1,1)
train_Yvar = np.concatenate((noise,noise_source))
train_Yvar = train_Yvar.reshape(-1,1)
print(train_X.shape)


# In[26]:


train_Y_trunc = train_Y[train_Y[:, 0]<=1000]
train_Yvar_trunc = train_Yvar[train_Y[:,0]<=1000]
train_X_trunc = train_X[train_Y[:, 0]<=1000, :]
print(train_X_trunc.shape)


# In[ ]:


model = SingleTaskMultiFidelityGP(torch.from_numpy(train_X_trunc), torch.from_numpy(train_Y_trunc), torch.from_numpy(train_Yvar_trunc), data_fidelities=[len(train_X_trunc[0]) - 1], input_transform=Normalize(d=4), outcome_transform=Standardize(m=1))
mll = ExactMarginalLogLikelihood(model.likelihood, model)
fit_gpytorch_mll(mll)


# In[ ]:


#Save trained model to disk
torch.save(model.state_dict(), 'my_model_multfidDFT16kwNoiseRefBetter.pth')

