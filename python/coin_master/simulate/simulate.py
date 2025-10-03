class Simulator:
    def __init__(self, reader, trader, visualizer, config):
        self.reader = reader
        self.trader = trader
        self.visualizer = visualizer
        self.config = config