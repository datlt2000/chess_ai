from ai.environments.manager import Environment
from gui.screens.Menu import Menu

evr = Environment()
ui = Menu()
ui.setManager(evr)
evr.setGUI(ui)
evr.start()