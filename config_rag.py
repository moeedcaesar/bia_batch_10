MODEL_NAME = "llama3"
EMBEDDING_MODEL = "nomic-embed-text"
DOCUMENT_PATH = "Data/rag_doc.pdf"
PROMPT_TEMPLATE = (
    "Your are a history expert. Use this history conversation: {history}\n"
    "Use this context from the document : {context}\n"
    "Answer the following question: {question}, keep it factual and under 100 words and end with short quiz"
)