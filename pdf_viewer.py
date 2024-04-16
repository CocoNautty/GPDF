from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QFileDialog, QPushButton
from PySide6.QtGui import QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from database import database
from pdf_editor import pdf_editor
from llm_api import llm_api
from ollm import ollm
import os

os.environ['no_proxy'] = '*'

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

        self.db = database()

        # self.llm = llm_api(api_key='sk-P987o6CLnxdvaUt06KjVjaOOoxPc5kTTGHHyD6vEoRdvkQ7F', proxy=None, base_url='https://api.chatanywhere.tech/v1/chat/completions', model='gpt-3.5-turbo', temperature=0.7)
        self.ollm = ollm(api_key='ollama', proxy=None, base_url='http://localhost:11434/v1', model='gemma', temperature=0.7)

    def create_file_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Choose PDF')
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)

        model_menu = menubar.addMenu('Switch Model')
        switch_gpt_action = QAction('Remote', self)
        switch_gpt_action.triggered.connect(self.switch_model_remote)
        model_menu.addAction(switch_gpt_action)
        switch_gemma_action = QAction('Local', self)
        switch_gemma_action.triggered.connect(self.switch_model_local)
        model_menu.addAction(switch_gemma_action)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        self.filename, _ = file_dialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if self.filename:
            self.webView.setUrl(QUrl("file:///" + self.filename.replace('\\', '/')))
    
    def switch_model_local(self):
            self.llm = llm_api(api_key='sk-nPGsvecBylzkSoeEbrRQ7k9dXb2X2uc7iiFRYDSfchMd773h', proxy=None, base_url='http://localhost:11434/api/chat', model='gemma:7b', temperature=0.7)
    
    def switch_model_remote(self):
            self.llm = llm_api(api_key='sk-nPGsvecBylzkSoeEbrRQ7k9dXb2X2uc7iiFRYDSfchMd773h', proxy=None, base_url='https://api.chatanywhere.tech/v1/chat/completions', model='gpt-3.5-turbo', temperature=0.7)
        

    def search_text(self, text):
        
        if '?' in text:
            self.webView.setUrl(QUrl("file:///" + self.filename.replace('\\', '/')))
            # TODO: Step 1: use chromadb to find related text
            result_book = self.db.search_book(text, 2)
            result_note = self.db.search_note(text, 1)
            material = result_book['documents'][0][0] + result_book['documents'][0][1] + result_note['documents'][0][0]

            # TODO: Step 2: call gpt to generate answer
            # ans = self.llm.send(text, material)
            ans = self.ollm.send(text, material)

            # TODO: Step 3: modify the pdf file to show the answer
            try:
                pdf_editor(self.filename, './files/temp.pdf', ans)
                # print("done")
                path=os.path.abspath('./files/temp.pdf')
                self.webView.setUrl(QUrl("file:///" + path.replace('\\', '/')))
            except Exception as e:
                print("Error", e)
        else:
            flag = QWebEnginePage.FindFlag.FindCaseSensitively
            if text:
                self.webView.page().findText(text, flag)
            else:
                self.webView.page().stopFinding()


            
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())