from abc import abstractmethod


class GeneticAlgorithm:

    def __init_subclass__(cls, **kwargs):
        pass

    def __init__(self, situation, action, population):
        """

        :param situation: tuple[] ex) [('arg', 90), ('range', 150), ......]
        :param action: tuple[]    ex) [('buy', 50), ('sale', 50),   ......]
        :param population int     ex) 100
        """
        self.__situation = situation
        self.__action = action
        self.__population = population

    @abstractmethod
    def init_population(self):
        pass

    @abstractmethod
    def generation(self, steps):
        """

        :param steps: int
        :return:
        """
        pass

    @abstractmethod
    def calc_fitness(self, steps):
        """

        :param steps: int
        :return:
        """
        pass

    @abstractmethod
    def determine_next_generation(self):
        pass

    @abstractmethod
    def obtain_situation(self):
        pass




