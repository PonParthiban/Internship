from llama_index.core.node_parser import (
    SentenceSplitter,          # split by sentences
    SemanticSplitterNodeParser, # split by meaning
    MarkdownNodeParser,        # split markdown smartly
    CodeSplitter,              # split code by functions
    HTMLNodeParser,            # split HTML by tags
)

# Sentence splitter
parser = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=50
)
nodes = parser.get_nodes_from_documents(docs)

# Semantic splitter (BEST)
# splits where MEANING changes, not just size
parser = SemanticSplitterNodeParser(
    embed_model=embed_model
)
nodes = parser.get_nodes_from_documents(docs)