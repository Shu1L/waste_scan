#coding=utf-8


class config(dict):
    def save(self, variableName, value):
        self[variableName] = value
    def getData(self, variableName):
        return self.get(variableName, None)
cfg = config()
