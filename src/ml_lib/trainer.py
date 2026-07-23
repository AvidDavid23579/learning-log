import torch
import torch.nn as nn

# Dataset
x = torch.linspace(-10, 10, 100).unsqueeze(1)
y = 2 * x + 1 

# Model
model = nn.Linear(1, 1)

criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

for epoch in range(1000):
    pred = model(x)
    loss = criterion(pred, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

print("Weight:", model.weight.item())
print("Bias:", model.bias.item())

# Save the trained model
torch.save(model.state_dict(), "models/linear.pt")