import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._choiceAlbum = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_hello(self, e):
        name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        try:
            totDint = int(self._view._txtInDurata.value)
        except ValueError:
            warnings.warn_explicit(message="durata non intera",
                                   category=Warning,
                                   filename="controller.py",
                                   lineno=15)
            return
        self._model.buildGraph(totDint)
        nodes = self._model.getNodes()
        for n in nodes:
            self._view._ddAlbum.options.append(ft.dropdown.Option(
                data=n,
                text=n.Title,
                on_click=self.getSelectedAlbum
            ))
        numNodi, numArchi = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {numNodi} nodi e {numArchi} spigoli"))
        self._view.update_page()


    def getSelectedAlbum(self, e):
        print("get selected album called")
        if e.control.data is None:
            self._choiceAlbum = None
        else:
            self._choiceAlbum = e.control.data
        print(self._choiceAlbum)

    def handleAnalisiComponente(self, e):
        if self._choiceAlbum is None:
            warnings.warn("Album not selected")
            return
        sizeC, totD = self._model.getConnessaDetails(self._choiceAlbum)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa che contiene {self._choiceAlbum}"
                                                      f"ha dimensioni {sizeC} "
                                                      f"e durata {totD}"))
        self._view.update_page()

    def handleGetSetAlbum(self, e):
        pass
