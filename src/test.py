from abc import abstractmethod

class A:
    def __init__(self,arg1=None,*bundle):
        try:
            self.initializer = bundle[0]
        except IndexError:
            # return empty dictionary
            self.initializer = {}
        try:
            self.a = self.initializer["Company"]
        except KeyError:
            print("No Bundle information passed.")
        self.conn = "con_string"

    def babu(self, name):
        print(self.conn + name)
