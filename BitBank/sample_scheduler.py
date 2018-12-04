from bitbank.scheduler import Scheduler
from bitbank.exceptions.schedcancel import SchedulerCancelException


class SampleRunner:

    def __init__(self):
        self.iteration = 0

    def __call__(self, *args, **kwargs):
        self.iteration += 1
        print('iteration: ' + str(self.iteration))
        if self.iteration == 3:
            raise SchedulerCancelException('iteration reaches number "3"')


if __name__ == '__main__':
    scheduler = Scheduler(runner=SampleRunner())
    print('Scheduler start')
    scheduler()
    print('Scheduler finish')
