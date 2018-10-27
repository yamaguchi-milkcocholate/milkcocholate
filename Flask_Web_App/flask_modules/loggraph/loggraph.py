class LogGraph:

    def __init__(self, population_id, plot_data):
        """

        :param population_id:
        :param plot_data:
        {
            'time': ['2018-10-23 00:00:00', ......],
            'position': ['98000', .......],
            'price': ['10080', ......],
        }
        """
        self.population_id = population_id
        self.plot_data = plot_data
