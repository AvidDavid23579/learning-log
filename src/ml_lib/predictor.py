import torch
import torch.nn as nn


class LinearPredictor:

    def __init__(self):

        self.model = nn.Linear(1, 1)

        self.model.load_state_dict(torch.load("models/linear.pt"))

        self.model.eval()

    def predict(self, x):

        x = torch.tensor([[x]], dtype=torch.float32)

        with torch.no_grad():
            y = self.model(x)

        return y.item()
