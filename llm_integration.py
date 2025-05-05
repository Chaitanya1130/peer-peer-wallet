from langchain_ollama import OllamaLLM

# Initialize the Ollama language model
llm = OllamaLLM(model="llama2", temperature=0.7)

# A simple prompt
prompt = "hello"

print("Sending prompt to Ollama...")
# Get the LLM's response
response = llm.invoke(prompt)
print("Received response from Ollama:")
# Print the response
print(response)