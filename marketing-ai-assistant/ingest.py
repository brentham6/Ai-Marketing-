from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

# Initialize Ollama models
llm = Ollama(model="llama2")
embed_model = OllamaEmbedding(model_name="llama2")

# Load your local documents
documents = SimpleDirectoryReader("docs").load_data()

# Build the index
index = VectorStoreIndex.from_documents(documents, llm=llm, embed_model=embed_model)

# Save to disk
index.storage_context.persist()

print("✅ Index saved to ./storage")
