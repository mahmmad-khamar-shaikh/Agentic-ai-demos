from langchain_community.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)


wiki_tool.run("What is LangChain?")

# Iniitilize Ollama llm
from langchain_ollama import Ollama
llm = Ollama(model="llama3.2:latest", base_url="http://localhost:11434")

tool = [wiki_tool]

# Tool binding
llm_with_tools = llm.bind_tools(tool)

# Call tools
response = llm_with_tools.invoke("What is LangChain?")
print(response)  # Print the response from the LLM with tool usage



