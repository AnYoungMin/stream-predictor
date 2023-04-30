import torch
import torch.nn as nn


class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers):
        super(LSTM, self).__init__()
        self.num_layers = num_layers
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(
            input_size, hidden_size, num_layers, batch_first=True
        )  # lstm cell, batch first=True (batch, seq, feature), False (seq, batch, feature)
        self.fc = nn.Linear(hidden_size, output_size, bias=True)

    def forward(self, x):
        h0 = torch.randn(
            (self.num_layers, x.size(0), self.hidden_size), requires_grad=True
        )  # if bidirec in future, multiplier flag 2 to num_layers
        c0 = torch.randn(
            (self.num_layers, x.size(0), self.hidden_size), requires_grad=True
        )
        out, _ = self.lstm(x, (h0, c0))  # out:  (batch, seq, hidden)
        out = self.fc(out[:, -1, :])
        return out
