import chromadb
from langchain_community.document_loaders import PyPDFLoader

class database:
    def __init__(self, path):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(name='mycollection')
        self.loader = PyPDFLoader(path)
        self.pages = self.loader.load_and_split()
        for page in self.pages:
            documents = [page.page_content]
            metadatas = [page.metadata]
            ids = [str(metadatas[0]['page'])]
            self.collection.add(documents=documents, metadatas=metadatas, ids=ids)

    def search_text(self, text, n):
        result = self.collection.query(
        query_texts=[text],
        n_results=n,
    )
