import torch
import torch.nn as nn
from torch.nn import init
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv
import torch_geometric.data as torchData

import numpy as np
import time
import random

import tqdm
import matplotlib.pyplot as plt 

from ConspiracySage_utils import *

class GraphSAGE(nn.Module) : 
    def __init__(self, num_node_features, num_classes):
        super(GraphSAGE, self).__init__()
        self.conv1 = SAGEConv(num_node_features, 16)
        self.conv2 = SAGEConv(16, num_classes)
        self.xent = nn.CrossEntropyLoss()
        # self.weight = nn.Parameter(torch.FloatTensor(num_classes, 11646)) # enc.embed_dim))
        # init.xavier_uniform(self.weight)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.2, training=self.training)
        return self.conv2(x, edge_index)# self.convs[-1](x, edge_index)

    def loss(self, pred, labels):
        return self.xent(pred, labels)  


def graphTest() : 
    # pytorch geometric data object, has attributes x, edge_index, and y
    data = load_YouTube() 

    rand_indices = np.random.permutation(x.shape[0])
    split = int(x.shape[0]*0.75)
    data.test_mask = torch.tensor(rand_indices[split:], dtype=torch.long)
    rand_indices = np.random.randint(0,x.shape[0],500)
    data.train_mask = torch.tensor(rand_indices, dtype=torch.long)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    num_classes = 4
    model = GraphSAGE(x.shape[1], num_classes).to(device)

    lr = 0.01
    weight_decay = 5e-4
    num_epochs = 25
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

    model.train()

    with open("Output.txt", "w") as text_file:
        print("Model Parameters: {} {}".format(lr, weight_decay), file=text_file)
        print("Trial Run", file=text_file)
        for epoch in tqdm.tqdm(range(num_epochs)):
            rand_indices = np.random.randint(0,x.shape[0],500)
            data.train_mask = torch.tensor(rand_indices, dtype=torch.long)
            optimizer.zero_grad()
            out = model(data.x, data.edge_index)

            if epoch % 10 == 0 : 
                _, pred = out.max(dim=1)
                correct = int(pred[data.test_mask].eq(data.y[data.test_mask]).sum().item())
                acc = correct / int(len(data.test_mask)) # int(data.test_mask.sum())
                print('Epoch: {0}, Accuracy: {1:.4f}'.format(epoch, acc), file=text_file)
            
            loss = model.loss(out[data.train_mask], data.y[data.train_mask])
            loss.backward()
            optimizer.step()

        model.eval()
        _, pred = model(data.x, data.edge_index).max(dim=1)
        correct = int(pred[data.test_mask].eq(data.y[data.test_mask]).sum().item())
        print("Sample of predictions:", file=text_file)
        print("pred", pred[data.test_mask][:20], file=text_file)
        print("real", data.y[data.test_mask][:20], file=text_file)
        acc = correct / int(len(data.test_mask))# int(data.test_mask.sum())
        print('Accuracy: {:.4f}'.format(acc))


    with open("test_model.pt", "wb") as model_file : 
        torch.save(model.state_dict(), model_file)

    return 


if __name__ == '__main__':
	# peek_adj()