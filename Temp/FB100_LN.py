from FB100 import FB100
class FB100_LN(FB100):
    __author__ = "Isaac Han"
    __email__ = "cogitoergosum01001@gmail.com"
    '''
    The model is LN(Liquid Nitrogen model). It operates between 80K ~ RT
    '''
    def __init__(self, port=None, channel=None):
        super().__init__(port, channel)

        lower = -200
        decimal = self.getTempDecimalSetting()
        self.instrument.set(float(f"{lower:.}"))