import numpy as np
import chainer
from chainer.backends import cuda
from chainer import Function, gradient_check, report, training, utils, Variable
from chainer import datasets, iterators, optimizers, serializers
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L
from chainer.training import extensions
from chainer.datasets import mnist
import time
from chainer.backends.cuda import to_cpu
import cupy as cp
from chainer.datasets import LabeledImageDataset
from chainercv.transforms import resize
from chainer.datasets import TransformDataset
import pickle

def transform(in_data):
    img, label = in_data
    img = resize(img, (28, 28))
    return img, label

train = LabeledImageDataset('data/train/train_labels.txt', 'data/train/images')
valid = LabeledImageDataset('data/valid/valid_labels.txt', 'data/valid/images')
test = LabeledImageDataset('data/test/test_labels.txt',   'data/test/images')
train = TransformDataset(train, transform)
valid = TransformDataset(valid, transform)
test = TransformDataset(test,   transform)

print(train)
print(valid)
print(test)

tmp_x = []
tmp_t = []
for i in range(train.__len__()):
    tmp_x.append(np.reshape(train.__getitem__(i)[0], (3, 28, 28)).astype(np.float32))
    tmp_t.append(train.__getitem__(i)[1].astype(np.int32))
x_train = np.array(tmp_x)
t_train = np.array(tmp_t)

tmp_x = []
tmp_t = []
for i in range(valid.__len__()):
    tmp_x.append(np.reshape(train.__getitem__(i)[0], (3, 28, 28)).astype(np.float32))
    tmp_t.append(valid.__getitem__(i)[1].astype(np.int32))
x_valid = (np.array(tmp_x))
t_valid = (np.array(tmp_t))

tmp_x = []
tmp_t = []
for i in range(test.__len__()):
    tmp_x.append(np.reshape(test.__getitem__(i)[0], (3, 28, 28)).astype(np.float32))
    tmp_t.append(test.__getitem__(i)[1].astype(np.int32))
x_test = (np.array(tmp_x))
t_test = (np.array(tmp_t))

print("Creating pickle file ...")
with open('x_train_np.pkl', 'wb') as f:
    pickle.dump(x_train, f)
print('Done!')
print("Creating pickle file ...")
with open('t_train_np.pkl', 'wb') as f:
    pickle.dump(t_train, f)
print('Done!')

print("Creating pickle file ...")
with open('x_test_np.pkl', 'wb') as f:
    pickle.dump(x_test, f)
print('Done!')
print("Creating pickle file ...")
with open('t_test_np.pkl', 'wb') as f:
    pickle.dump(t_test, f)
print('Done!')
"""

print(chainer.cuda.available)
start = time.time()

with open('x_train.pkl', 'rb') as f:
    x_train = pickle.load(f)

with open('t_train.pkl', 'rb') as f:
    t_train = pickle.load(f)

with open('x_test.pkl', 'rb') as f:
    x_test = pickle.load(f)

with open('t_test.pkl', 'rb') as f:
    t_test = pickle.load(f)

gpu_id = 0


class LeNet5(Chain):
    def __init__(self):
        super(LeNet5, self).__init__()
        with self.init_scope():
            self.conv1 = L.Convolution2D(
                in_channels=3, out_channels=6, ksize=5, stride=1)
            self.conv2 = L.Convolution2D(
                in_channels=6, out_channels=16, ksize=4, stride=1)
            self.conv3 = L.Convolution2D(
                in_channels=16, out_channels=126, ksize=4, stride=1)
            self.fc4 = L.Linear(None, 84)
            self.fc5 = L.Linear(84, 10)

    def __call__(self, x):
        h = F.sigmoid(self.conv1(x))
        h = F.max_pooling_2d(h, 2, 2)
        h = F.sigmoid(self.conv2(h))
        h = F.max_pooling_2d(h, 2, 2)
        h = F.sigmoid(self.conv3(h))
        h = F.sigmoid(self.fc4(h))
        if chainer.config.train:
            return self.fc5(h)
        return F.softmax(self.fc5(h))


model = LeNet5()


if gpu_id >= 0:
    model.to_gpu(gpu_id)
optimizer = optimizers.Adam()
optimizer.setup(model)

batch_size = 100
max_iteration = 10000
data_size = x_train.shape[0]
epoch = 0

for iteration in range(max_iteration):
    batch_mask = np.random.choice(data_size, batch_size)
    x_batch = Variable(cp.asarray(x_train[batch_mask]))
    t_batch = Variable(cp.asarray(t_train[batch_mask]))
    y = model(x_batch)
    loss = F.softmax_cross_entropy(y, t_batch)
    model.cleargrads()
    loss.backward()
    optimizer.update()
    if (iteration * batch_size) % data_size == 0:
        epoch += 1
        accuracy = F.accuracy(y, t_batch)
        accuracy.to_cpu()
        train_loss = float(to_cpu(loss.data))
        train_accuracy = float(to_cpu(accuracy.data))
        print('epoch: {:02d} train_loss:{:.04f} train_accuracy:{:.04f}'
              .format(epoch, train_loss, train_accuracy))

y = model(x_test)
prediction_test = F.softmax_cross_entropy(y, t_test)
accuracy = F.accuracy(y, t_test)
accuracy.to_cpu()
valid_loss = float(to_cpu(prediction_test.data))
valid_accuracy = float(to_cpu(accuracy.data))
print('valid_los:{:.04f} valid_accuracy:{:.04f}'.format(valid_loss, valid_accuracy))

serializers.save_npz('Convolutional_1.model', model)
serializers.save_npz('Convolutional_1.state', optimizer)
timer = time.time() - start
print(("time:{0}".format(timer)), "[sec]")
"""
