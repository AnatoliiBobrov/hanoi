from copy import deepcopy
import pickle
import torch
from torch import optim
import torch.nn as nn
import torch.nn.functional as F

# коды перемещений колец:
# куда  0  1  2
# из 0     0  1
# из 1  2     3
# из 2  4  5  
CODE_TABLE = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
EMPTY_LIST = [] # пустой список
RINGS = 5 # количество колец
EPOCHES = 200 # количество эпох
LEARNING_RATE = 0.005 # коэффициент обучения
SORTED_TOWER = list(range(RINGS, 0, -1)) # сортированная башня

def move(towers, move_code):
    """
    Производит указанное перемещение
    """
    from_, to_ = CODE_TABLE[move_code]
    towers[to_].append(towers[from_].pop())   

def to_tensor(towers):
    """
    Возвращает тензорное представление текущей ситуации
    """
    result = torch.zeros(3 * RINGS)
    for i, tower in enumerate(towers):
        result[i * RINGS:i * RINGS + len(tower)] = torch.tensor(tower)
    return result

class Net(nn.Module):
    def __init__(self):
        """
        Создает простой многослойный перцептрон
        """
        super(Net, self).__init__()
        coef = 60 * RINGS
        self.input_layer = nn.Linear(3 * RINGS, coef)
        self.hidden_layer = nn.Linear(coef, coef)
        self.s_hidden_layer = nn.Linear(coef, 6)
        
    def forward(self, x):
        """
        Возвращает результат работы нейронной сети
        """
        x = F.relu(self.input_layer(to_tensor(x)))
        x = F.relu(self.hidden_layer(x))
        x = self.s_hidden_layer(x)
        return F.softmax(x)

def get_trained_network():
    """
    Возвращает обученную нейронную сеть
    """
    a = pickle.load(open("data.bin", "rb"))
    tasks, targets = a
    net = Net() # экземпляр нейронной сети
    # Осуществляем оптимизацию путем стохастического градиентного спуска
    optimizer = optim.SGD(net.parameters(), lr=LEARNING_RATE, momentum=0.9)
    # Создаем функцию потерь
    criterion = nn.MSELoss()
    epoch = 0
    accuracy = 0
    counter = 0
    # запускаем главный тренировочный цикл
    for epoch in range(EPOCHES):
        accuracy = 0
        counter = 0
        for i, towers_1 in enumerate(tasks):
            counter += len(targets[i])
            towers = deepcopy(towers_1)
            for m in targets[i]:
                net_out = net(towers)
                inds = torch.argmax(net_out).item()
                target = torch.tensor([0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
                target[m] = 0.99
                if m == inds:
                    accuracy += 1
                else:
                    loss = criterion(net_out, target)
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                move(towers, m)
        accuracy_p = accuracy / counter * 100
        if accuracy == counter: 
            break
    print (f"Epochs: {epoch}, accuracy: {accuracy_p:.2f}%, amount: {counter}")
    pickle.dump(net, open("network.bin", "wb"))
    return net

get_trained_network()
