import mysql.connector
from sqlalchemy import create_engine, text, inspect
import openai
import json

# Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "zxcvbnmmnbvcxz1",
    "database": "agriculture_datalabs",
}

# Construct the connection string
connection_string = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

# Create an engine instance
engine = create_engine(connection_string)
inspector = inspect(engine)
tables = inspector.get_table_names()

# Table Details
table_details = {
    "fertilizer": "stores fertilizer data.",
    "crop_production": "stores crop production data.",
    "temperature": "stores temperature data.",
    "final_rainfall": "stores finalized rainfall data.",
    "final_temperature": "stores finalized temperature data.",
    "rainfall_validation": "stores rainfall validation data, with subdivision",
    "data_after_rainfall": "stores data collected post rainfall.",
    "crop_yield": "stores crop yield data, and the production",
    "final_dataset_after_temperature": "stores final dataset post temperature analysis."
}

from llama_index import SQLDatabase, ServiceContext, LLMPredictor, OpenAIEmbedding, PromptHelper
from llama_index.llms import OpenAI
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine
from llama_index.objects import ObjectIndex, SQLTableNodeMapping, SQLTableSchema
from llama_index.indices.struct_store import SQLTableRetrieverQueryEngine

# Initializing necessary components
sql_database = SQLDatabase(engine, sample_rows_in_table_info=2)

openai.api_key = "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"  # Replace with your actual OpenAI API key

llm = OpenAI(temperature=0, model="gpt-4")
service_context = ServiceContext.from_defaults(llm=llm)

table_node_mapping = SQLTableNodeMapping(sql_database)
table_schema_objs = [(SQLTableSchema(table_name=table, context_str=table_details[table])) for table in tables]

obj_index = ObjectIndex.from_objects(
    table_schema_objs,
    table_node_mapping,
    service_context=service_context
)

query_engine = SQLTableRetrieverQueryEngine(
    sql_database, obj_index.as_retriever(similarity_top_k=3), service_context=service_context
)

class ChatHistory:
    def __init__(self):
        self.history_file = 'chat_history.json'
        self.clear_history()  # Clear the history on initialization

    def clear_history(self):
        self.history = []
        with open(self.history_file, 'w') as file:
            json.dump(self.history, file, indent=4)

    def save_history(self):
        with open(self.history_file, 'w') as file:
            json.dump(self.history, file, indent=4)

    def add_to_history(self, query, response):
        self.history.append({'query': query, 'response': response})
        self.save_history()

    def get_history(self):
        return self.history



# Create a global instance of ChatHistory
chat_history = ChatHistory()

stored_chat_history = chat_history.get_history()

print(stored_chat_history)
def get_chat_history():  # Define get_chat_history() to return the chat history
    return chat_history.get_history()

def query_db(query_str):
    # Convert the stored_chat_history to a formatted string
    chat_history_str = '\n'.join([f"User: {entry['query']}\nBot: {entry['response']}" for entry in stored_chat_history])

    # Now prepend chat_history_str to the prompt
    prompt = f"{chat_history_str}\n\nUser: {query_str}\nBot:"

    # The rest of your code...
    response = query_engine.query(prompt)
    response_str = str(response)  # ensure response is converted to string
    chat_history.add_to_history(query_str, response_str)  # save to history
    return {'query': query_str, 'response': response_str}

# Now when you call query_db, the stored_chat_history will be included in the prompt


