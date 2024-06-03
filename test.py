from model.model import Model

myModel = Model()
myModel.buildGraph(120*60*1000)
print(myModel.getGraphDetails())
