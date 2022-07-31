import random


class rating:
    def __init__(self) -> None:
        self.log = []
        pass

    def indexVal(self, index):
        i = random.randint(0,index - 1)
        if len(self.log) > index:
            self.log.pop(0)
        for x in range(0,len(self.log)):
            if i in self.log:
                #print("Re-eval")
                i = (i + random.randint(0,index - 1)) % index
        self.log.append(i)
        return i

    def procure(self, rating):
        f = open('/Users/nitinrajesh/Code/FantomCode/FC11-404/flask_app/lookup/truthRatings.txt',mode='r')
        words = f.read().splitlines()
        word = words[self.indexVal(len(words))]
        f.close()
        return word