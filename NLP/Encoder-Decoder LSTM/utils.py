# -*- coding: utf-8 -*-
"""utils

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PWBnYBU6Q5GGSnN_Z_luOgOFjNb-JFCU
"""

import torch

def load_checkpoint(checkpoint, model, optimizer):
    model.load_state_dict(checkpoint["state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer"])
    return model, optimizer

def save_checkpoint(state, path, name):
    torch.save(state, path + name + '.pth')

def i2w(tensor, vocab, target=False):
    batch = [] # list of all sentances
    for sentence in range(tensor.shape[1]):
        sen = [] # list of one sentance converted from tensor with indexes to list with words
        for idx in tensor[1:,sentence]:
            word = vocab.vocab.itos[int(idx)]
            if word != '<eos>':
                sen.append(word)
            else:
                break
        if target:
            batch.append([sen]) # to calculate bleu score the target sentance needs to be in list
        else:
            batch.append(sen)
    return batch