from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

class HistoryChatBot:
    def __init__(self, model_name, prompt_template):
        """
        This is an initialize function for a history chatbot
        :param model_name: Name of the model
        :param prompt_template: Entire Context of the prompt (Prompt Engineering)
        """

        self.llm = Ollama(model=model_name)
        self.prompt = PromptTemplate.from_template(prompt_template)
        self.memory = ConversationBufferMemory()
        self.chain = ConversationChain(
            llm = self.llm,
            memory = self.memory,
            prompt = self.prompt,
            input_key ="input")

    def get_response(self, user_input):
        return self.chain.predict(input = user_input)

    def clear_memory(self):
        self.memory.clear()