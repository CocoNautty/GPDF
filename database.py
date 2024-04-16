import chromadb
from langchain_community.document_loaders import PyPDFLoader

class database:
    def __init__(self):
        # self.client = chromadb.Client()
        # self.collection = self.client.create_collection(name='mycollection')
        # self.loader = PyPDFLoader(path)
        # self.pages = self.loader.load_and_split()
        # for page in self.pages:
        #     documents = [page.page_content]
        #     metadatas = [page.metadata]
        #     ids = [str(metadatas[0]['page'])]
        #     self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
        try:
            self.client = chromadb.PersistentClient(path="./data")
            self.collection_book = self.client.get_collection(name="book")
            self.collection_note = self.client.get_collection(name="note")
        except:
            self.client = chromadb.PersistentClient(path="./data")
            self.collection_book = self.client.create_collection(name="book")
            self.collection_note = self.client.create_collection(name="note")
            loader = PyPDFLoader('./files/book.pdf')
            pages = loader.load_and_split()
            for page in pages:
                documents = [page.page_content]
                metadatas = [page.metadata]
                ids = [str(metadatas[0]['page'])]
                self.collection_book.add(documents=documents, metadatas=metadatas, ids=ids)
            loader = PyPDFLoader('./files/note.pdf')
            pages = loader.load_and_split()
            for page in pages:
                documents = [page.page_content]
                metadatas = [page.metadata]
                ids = [str(metadatas[0]['page'])]
                self.collection_note.add(documents=documents, metadatas=metadatas, ids=ids)

    def search_book(self, text, n):
        return self.collection_book.query(
        query_texts=[text],
        n_results=n,
        )
    
    def search_note(self, text, n):
        return self.collection_note.query(
        query_texts=[text],
        n_results=n,
        )
