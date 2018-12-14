from modules.fitnessfunction.inclination_optimization import InclinationOptimization


inclination_optimization = InclinationOptimization(
    sma_term=20,
    std_term=20,
    stock_term=20,
    inclination_alpha=9,
    target='simple_moving_average',
)
inclination_optimization()
