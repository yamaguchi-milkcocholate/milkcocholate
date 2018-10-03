from chainer.datasets import LabeledImageDataset
from chainercv.transforms import resize
from chainer.datasets import TransformDataset
from chainer.training import extensions
from chainer import training, iterators, optimizers, Chain
import chainer.functions as F
import chainer.links as L
import chainer
import time

def transform(in_data):
    img, label = in_data
    img = resize(img, (50, 50))
    return img, label

start = time.time()
print(chainer.cuda.available)
train = LabeledImageDataset('data/train/train_labels.txt', 'data/train/images')
valid = LabeledImageDataset('data/valid/valid_labels.txt', 'data/valid/images')
test  = LabeledImageDataset('data/test/test_labels.txt',   'data/test/images')

train = TransformDataset(train, transform)
valid = TransformDataset(valid, transform)
test = TransformDataset(test,   transform)

batch_size = 100
train_iter = iterators.SerialIterator(train, batch_size)
test_iter = iterators.SerialIterator(test, batch_size, False, False)

class MLP(Chain):

    def __init__(self, n_mid_units=100, n_out=10):
        super(MLP, self).__init__()
        with self.init_scope():
            self.l1 = L.Linear(None, n_mid_units)
            self.l2 = L.Linear(None, n_mid_units)
            self.l3 = L.Linear(None, n_out)

    def __call__(self, x):
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        return self.l3(h2)

gpu_id = 0

model = MLP()
if gpu_id >= 0:
    model.to_gpu()

max_epoch = 10

model = L.Classifier(model)
optimizer = optimizers.Adam()

optimizer.setup(model)
updater = training.updaters.StandardUpdater(train_iter, optimizer, device=gpu_id)

trainer = training.Trainer(updater, (max_epoch, 'epoch'))
trainer.extend(extensions.LogReport())
trainer.extend(extensions.snapshot(filename='snapshot_epoch-{.updater.epoch}'))
trainer.extend(extensions.snapshot_object(model.predictor, filename='model_epoch-{.updater.epoch}'))
trainer.extend(extensions.Evaluator(test_iter, model, device=gpu_id))
trainer.extend(extensions.PrintReport(['epoch', 'main/loss', 'main/accuracy', 'validation/main/loss', 'validation/main/accuracy', 'elapsed_time']))
trainer.extend(extensions.PlotReport(['main/loss', 'validation/main/loss'], x_key='epoch', file_name='loss.png'))
trainer.extend(extensions.PlotReport(['main/accuracy', 'validation/main/accuracy'], x_key='epoch', file_name='accuracy.png'))
trainer.extend(extensions.dump_graph('main/loss'))

trainer.run()
timer = time.time() - start
print(("time:{0}".format(timer)), "[sec]")
