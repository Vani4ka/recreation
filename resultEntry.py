class ResultEntry:
    far = 100.0
    mr = 100.0
    featureSet = []

    def __init__(self, far=1.0, mr=1.0, fs=[]):
        self.far = far*100.0
        self.mr = mr*100.0
        self.featureSet = fs
