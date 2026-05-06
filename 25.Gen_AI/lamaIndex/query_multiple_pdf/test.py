import fitz  # pymupdf

pdf_path = "./data/restapi_doc.pdf"
doc = fitz.open(pdf_path)

print(f"Pages: {len(doc)}")
print(f"Encrypted: {doc.is_encrypted}")
print(f"\nFirst 300 chars of page 1:")
print(doc[0].get_text()[:300])