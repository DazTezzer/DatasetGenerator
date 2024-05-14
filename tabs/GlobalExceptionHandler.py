import sys
import traceback
from ui.UI_MainWindow import Ui_MainWindow


class GlobalExceptionHandler:
    def __init__(self, main_window_ui: Ui_MainWindow):
        super().__init__()
        self.ui = main_window_ui
        sys.excepthook = self.handle_exception

    def handle_exception(self, ex_type, ex_value, ex_traceback):
        text = "Глобальный обработчик исключений:\n"
        text += f"Тип исключения: {ex_type}\n"
        text += f"Значение исключения: {ex_value}\n"
        traceback.print_tb(ex_traceback)
        self.ui.globalExceptionHandlerPlainTextEdit.appendPlainText(text)
