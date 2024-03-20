from ui_mediator import Mediator
from converter_ui import ConverterUI

if __name__ == "__main__":
    mediator = Mediator()
    converter_ui = ConverterUI(mediator)
    converter_ui.run()