from models.assets import AssetsCollector


assets_collector = AssetsCollector(host='localhost')
assets_collector.show_plot(
    start='2018-12-13 18:00:00',
    end='2018-12-13 20:30:00',
    coin='jpy'
)
