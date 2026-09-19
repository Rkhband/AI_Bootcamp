from pypdf import PdfReader

#doc_path = 'docs/hr_policy.pdf'


def create_chunks(doc_path,chunk_size=500,overlap_size=100):
    reader = PdfReader(doc_path)
    full_text = ''
    for page in reader.pages:
        text = page.extract_text()
        full_text = full_text + text + '\n'

    chunks = []
    start = 0
    while start < len(full_text):
        end = start + chunk_size
        chunk = full_text[start:end]
        chunks.append(chunk)
        start = end - overlap_size
    return chunks


# chunks = create_chunks(doc_path,500,100)

# print(len(chunks))

# print(chunks[50])


