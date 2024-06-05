from model.model import Model

myModel = Model()
myModel.buildGraph(120*60*1000)
print(myModel.getGraphDetails())

myModel.get_set_album(myModel.getNodeI(1), 9000)