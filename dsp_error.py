class DSPError(BaseException):

    def __init__(self, device, mesg):
        self.device = device
        self.mesg = mesg

    def __str__(self):
        return '%s: %s' % (self.device, self.mesg)
