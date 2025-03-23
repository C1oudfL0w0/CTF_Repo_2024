import time
class User():
    def __init__(self,name,password):
        self.name=name
        self.pwd = password
        self.Registertime=str(time.time())[0:10]
        self.handle=None

        self.secret=self.setSecret()

    def handler(self):
        self.handle = open("/dev/random", "rb")
    def setSecret(self):
        secret = self.Registertime
        try:
            if self.handle == None:
                self.handler()
            secret += str(self.handle.read(22).hex())
        except Exception as e:
            print("this file is not exist or be removed")
        return secret