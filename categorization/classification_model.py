import torch
import torch.nn as nn
import math

class CustomDataset(torch.utils.data.Dataset):

    def __init__(self, df, target_list):
        self.df = df
        self.vectors = df['vector'].values
        self.targets = self.df[target_list].values

    def __len__(self):
        return len(self.vectors)

    def __getitem__(self, index):
        return torch.FloatTensor(self.vectors[index]), torch.FloatTensor(self.targets[index])
    
    
def train_test_datasets(train, test, target_list):
    train_custom = CustomDataset(train, target_list)
    test_custom = CustomDataset(test, target_list)
    
    train_loader = torch.utils.data.DataLoader(train_custom, 
        batch_size=128,
        shuffle=True
    )

    test_loader = torch.utils.data.DataLoader(test_custom, 
        batch_size=128,
        shuffle=False
    )
    
    return train_loader, test_loader


def get_test_loader(test, target_list):
    test_custom = CustomDataset(test, target_list)
    test_loader = torch.utils.data.DataLoader(test_custom, 
        batch_size=128,
        shuffle=False
    )
    
    return test_loader
    
class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(100, 512),
            nn.Tanh(),
            nn.Linear(512, 512),
            nn.Tanh(),
            nn.Linear(512, 11),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits
    
def train_nn(model, train_loader, criterion, optimizer, epochs, history):
    for i in range(epochs):
        for x_batch, y_batch in train_loader:
            # 1. # загружаем батч данных (вытянутый в линию)
            x_batch = x_batch.view(x_batch.shape[0], -1)
            y_batch = y_batch

            # 2. вычисляем скор с помощью прямого распространения ( .forward or .__call__ )
            logits = model(x_batch)

            # 3. вычислеяем - функцию потерь (loss)
            loss = criterion(logits, y_batch)
            history.append(loss.item())

            # 4. вычисляем градиенты
            optimizer.zero_grad()
            loss.backward()

            # 5. шаг градиентного спуска
            optimizer.step()

        print(f'{i+1}\t loss: {history[-1]}')
        
def predict(model, test_loader):
    all_predictions = []
    for x_batch, y_batch in test_loader:
        for i in model(x_batch):

            predictions_probabilities = i.detach().numpy()
            best_prediction = predictions_probabilities.argsort()[::-1][0]
            best_prediction_value = max(predictions_probabilities)
            predictions = [best_prediction]
            for j in range(len(predictions_probabilities)):
                if ((best_prediction_value - predictions_probabilities[j]) <= 1.5) and (best_prediction != j):
                    predictions.append(j)

            all_predictions.append(predictions)
    return all_predictions


def multilabel_accuracy(predictions, target):
    assert(len(predictions) == len(target))
    
    # за одно наблюдение можно получить максимум 1 балл
    # 1 балл получается, если все предсказания для одного наблюдения совпали с target_i
    # иначе считается, сколько предсказаний совпало и делится на длину target_i
    points = 0.0
    for i in range(len(predictions)):
        # если количество предсказанных меток больше, чем количество реальных меток, нужно делить на длину predictions[i]
        if len(target[i]) < len(predictions[i]):
            point = len(set(predictions[i]) & set(target[i]))/len(predictions[i])
        else:    
            point = len(set(predictions[i]) & set(target[i]))/len(target[i])
        points += point
    return points/len(target)
        
        





