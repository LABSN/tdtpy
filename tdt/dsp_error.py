class DSPError(Exception):

    def __init__(self, device, mesg):
        self.device = device
        self.mesg = mesg

    def __str__(self):
        return '{}: {}'.format(self.device, self.mesg)
