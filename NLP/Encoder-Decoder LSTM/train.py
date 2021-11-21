# -*- coding: utf-8 -*-
"""training_loop.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C83dl-RUF9zXDKVZuaW66J_GdFKRpILi
"""

import torch
import torch.nn as nn
from utils import load_checkpoint, save_checkpoint, i2w, datasetGenerator
from model import Model
from seq2seq import Seq2Seq, Encoder, Decoder
from tqdm.notebook import tqdm_notebook
import matplotlib.pyplot as plt
#from google.colab import drive => uncomment for colab
#drive.mount('/content/drive')

BATCH = 128
LEARNING_RATE = 0.001
LAYERS = 2
HIDDEN_DIM = 256
EPOCHS = 25
EMBEDDING_DIM = 300
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
P = 0.5 

# DATASET
(train_iterator, validation_iterator, test_iterator), (train_data, validation_data, test_data), (english, german) = datasetGenerator(BATCH, DEVICE, 30*128)

# MODEL
ENCODER = Encoder(input_size=len(german.vocab), embedding_size=EMBEDDING_DIM, 
                  hidden_size=HIDDEN_DIM, layers=LAYERS, p=P, bidirectional=False).to(DEVICE)

DECODER = Decoder(input_size=len(english.vocab), output_size=len(english.vocab), 
                  embedding_size=EMBEDDING_DIM, hidden_size=HIDDEN_DIM,
                  layers=LAYERS, p=P, bidirectional=False).to(DEVICE)

SEQ2SEQ = Seq2Seq(ENCODER, DECODER).to(DEVICE)
MODEL = Model(model=SEQ2SEQ, lr=LEARNING_RATE, vocab=english, device=DEVICE)
STEPLR = torch.optim.lr_scheduler.StepLR(MODEL.opt, step_size=10, gamma=0.5)

# TRAINING LOOP
force_ratio = 0.5
train_loss, train_bleu = [], [0]
val_loss, val_bleu = [], [0] # added zero at the start to avoid error with max
lr = []
for epoch in tqdm_notebook(range(1, 25+1), desc = 'Epoch'):
    tl, tb = MODEL.train_step(train_iterator, force_ratio)
    vl, vb = MODEL.validation_step(validation_iterator)

    if vb > max(val_bleu):
        save_checkpoint(MODEL.checkpoint, 'drive/MyDrive/model128')
    
    if epoch%5 == 0 and force_ratio > 1e-6:
        force_ratio = force_ratio * 0.5

    STEPLR.step()

    train_loss.append(tl)
    train_bleu.append(tb)
    val_loss.append(vl)
    val_bleu.append(vb)
    lr.append(STEPLR.get_lr())
    
    
    #print(f'Bleu score: {tb}, {vb}')
    #print(f'Learning rate: {lr[-1]} Force ratio : {force_ratio}')

MODEL.test_step(test_iterator)

plt.figure(dpi=200)
plt.grid()
plt.plot(train_loss, label='Training')
plt.plot(val_loss, label='Validation')
plt.savefig('drive/MyDrive/loss.png')

plt.figure(dpi=200)
plt.grid()
plt.plot(train_bleu, label='Training')
plt.plot(val_bleu, label='Validation')
plt.savefig('drive/MyDrive/bleu.png')