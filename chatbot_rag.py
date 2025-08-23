import re
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma

class HistoryChatBot:
    def __init__(self, model_name, prompt_template, embedding_model, document_path):
        """
        This is an initialize function for a history chatbot
        :param model_name: Name of the model
        :param prompt_template: Entire Context of the prompt (Prompt Engineering)
        """

        self.llm = Ollama(model=model_name)
        self.embeddings = OllamaEmbeddings(model=embedding_model)
        self.memory = ConversationBufferMemory(input_key='question', memory_key='history')
        self.prompt = PromptTemplate.from_template(prompt_template)
        self.rag_chain = self._setup_rag(document_path)

    def _setup_rag(self, document_path):
            loader = PyPDFLoader(document_path)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = text_splitter.split_documents(documents)
            vector_store = Chroma.from_documents(chunks, self.embeddings, collection_name='history_facts')
            return RetrievalQA.from_chain_type(
                llm = self.llm,
                chain_type='stuff',
                retriever = vector_store.as_retriever(search_kwargs={"k":3}),
                return_source_documents = True,
                chain_type_kwargs = {"prompt": self.prompt, "memory": self.memory}
            )

    def is_history_related(self, user_input):
        """
        To check if the user prompt is related to the History or the documents ?
        :param user_input:
        :return:
        """
        user_input_lower = user_input.lower().strip()
        temporal_pattern = r'\b(\d{3,4})\b|\b(\d{1,2}(?:th|st|nd|rd)\s+century)\b|\b(bc|ad)\b|\b(long ago|in the past|ancient times)\b'
        if re.search(temporal_pattern, user_input_lower):
            return True
        event_pattern = r'\b(battle of|fall of|rise of|treaty of|revolution of|conquest of|independence of)\b'
        if re.search(event_pattern, user_input_lower):
            return True
        words = user_input.split()
        if len(words)>1 and any(word[0].isupper() for word in words[1:]):
            return True

        return False

    def get_response(self, user_input):
        if not self.is_history_related(user_input):
            return "This is off topic Question!"
        result = self.rag_chain.invoke({"query":user_input})
        return result['result']

    def clear_memory(self):
        self.memory.clear()