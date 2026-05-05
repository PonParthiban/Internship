from llama_index.core import SimpleDirectoryReader
from llama_index.readers.web import SimpleWebPageReader
from llama_index.readers.youtube import YoutubeTranscriptReader
from llama_index.readers.notion import NotionPageReader
from llama_index.readers.database import DatabaseReader

# Load entire folder
docs = SimpleDirectoryReader("./data").load_data()
# loads PDFs, Word, txt, CSV, images automatically

# Load website
docs = SimpleWebPageReader().load_data(["https://example.com"])

# Load YouTube
docs = YoutubeTranscriptReader().load_data(
    ytlinks=["https://youtube.com/watch?v=xxx"]
)

# Load database
docs = DatabaseReader(
    sql_database=db
).load_data(query="SELECT * FROM products")