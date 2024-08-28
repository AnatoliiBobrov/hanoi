Перевод на английском ниже
В файле "data.bin" хранится все возможные несортированные ханойские 
башни с 5 кольцами и их кратчайшие решения в виде двух списков. 
Первый из них множество задач, второй - соответствующие решения. 
Генератор таких задач и решений к ним: файл "hanoi generator.py". 
Решения формируются методом грубой силы, где производится перебор 
возможных ходов (если есть "хорошие", то из числа хороших),
при этом выбирается наикратчайший путь решения. Это может занять 
около 2 часов на не самом мощном компьютере.

Решения состоят из последовательности закодированных ходов. Ниже 
представлена кодовая таблица:

```
куда  0  1  2
из 0     0  1
из 1  2     3
из 2  4  5 
```

0, 1, 2 - номера стержней
0 - "источник", 1 - целевой стержень, 2 - вспомогательный.

Файл "hanoi training.py" обучает нейронную сеть на наборе задач из
"data.bin". Нейроная сеть - полносвязный многослойный перцептрон.
Чтобы улучшить запоминание решений, мы отказались от уменьшения 
ошибки: если нейронная сеть правильно вспомнила решение, поправка
весов нейронной сети не производится, в противном случае производится
корректировка весов. Таким образом, получилось достичь точности в 100%
на наборе из 1776 ходов в сумме для 120 вариантов Ханойской башни из
5 колец.

English
The "data.bin" file stores all possible unsorted Hanoi
towers with 5 rings and their shortest solutions in the form of two lists. 
The first of them is a set of tasks, the second is the appropriate solutions. 
A generator of such problems and solutions to them: the file "hanoi generator.py
Solutions are formed by the brute force method, where
possible moves are sorted out (if there are "good" ones, then from among the good ones),
while the shortest solution path is chosen. It may take
about 2 hours on a not very powerful computer.

The solutions consist of a sequence of coded moves. Below 
The code table is presented:

``
where 0 1 2
from 0 0 1
out of 1 2 3
out of 2 4 5 
```

0, 1, 2 - rod numbers
0 - "source", 1 - target rod, 2 - auxiliary.

The file "hanoi training.py " trains a neural network on a set of tasks from
"data.bin". A neural network is a fully connected multi-layered perceptron.
To improve the memorization of decisions, we refused to reduce 
errors: if the neural network remembers the decision correctly, the correction
of the weights of the neural network is not performed, otherwise
the weights are adjusted. Thus, it turned out to achieve an accuracy of 100%
on a set of 1776 moves for a total of 120 variants of the Tower of Hanoi
5 rings.
