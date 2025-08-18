MODEL_NAME = "llama3"
PROMPT_TEMPLATE = (
    "Your are a history expert. Use this history conversation: {history}\n"
    "Answer the question: {input}. Keep it factual, fun and in less than 100 words"
    "and add a quiz question in the end related to the topic"
)