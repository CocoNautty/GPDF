from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QFileDialog, QPushButton
from PySide6.QtGui import QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from database import database
from pdf_editor import pdf_editor

class SearchLineEdit(QLineEdit):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Return:
            self.main_window.search_text(self.text())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Viewer")
        self.setGeometry(0, 28, 1000, 750)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.webView = QWebEngineView()
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PluginsEnabled, True)
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PdfViewerEnabled, True)
        self.layout.addWidget(self.webView)
        
        self.search_input = SearchLineEdit(self)
        self.search_input.setPlaceholderText("Enter text to search...")
        self.layout.addWidget(self.search_input)

        self.create_file_menu()

    def create_file_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Choose PDF')
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        self.filename, _ = file_dialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if self.filename:
            self.webView.setUrl(QUrl("file:///" + self.filename.replace('\\', '/')))
            self.db = database(self.filename)
        

    def search_text(self, text):
        flag = QWebEnginePage.FindFlag.FindCaseSensitively
        if text:
            self.webView.page().findText(text, flag)
        else:
            self.webView.page().stopFinding()

        # TODO: Step 1: use chromadb to find related text
        result = self.db.search_text(text, 5)

        # TODO: Step 2: call gpt to generate answer

        # TODO: Step 3: modify the pdf file to show the answer
        ans = '...'
        try:
            self.webView.setUrl(QUrl(""))
            pdf_editor(self.filename, self.filename, ans)
            print("done")
            self.webView.setUrl(QUrl("file:///" + self.filename.replace('\\', '/')))
        except Exception as e:
            print("Error", e)


            
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())