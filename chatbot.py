from typing import List, Dict
from langgraph.graph import StateGraph, START, END
from langchain_ollama.llms import OllamaLLM


# Step 1: Define the states and transitions for the chatbot
class State(Dict):
    messages: List[Dict[str, str]]


# Step 2: Initialize the state graph
graph_builder = StateGraph(State)

# Step 3 : Initialize the LLM
llm = OllamaLLM(model="llama3.2:latest", temperature=0)


# Step 4: Define Chatbot function
# Step 4: Define Chatbot function
def chatbot(state: State) -> State:
    response = llm.invoke(state["messages"])
    # Check if the response is a string or an object with a 'content' attribute
    if isinstance(response, str):
        state["messages"].append({"role": "assistant", "content": response})
    else:
        state["messages"].append({"role": "assistant", "content": response.content})
    return state  # Return the updated state dictionary


# Add nodes and edesges to the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Step 5: Compile the Graph.
graph = graph_builder.compile()


# Stream Update
def stream_graph_update(user_input: str):
    # Initialize the state with user input
    state = {"messages": [{"role": "user", "content": user_input}]}
    # Execute the graph
    for event in graph.stream(state):
        for value in event.values():
            # Print the assistant's message
            print("Assistant:", value["messages"][-1]["content"])


# Run the chatbot with user input
if __name__ == "__main__":
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "bye", "q"]:
                print("Exiting the chatbot. Goodbye!")
                break
            stream_graph_update(user_input)
        except Exception as e:
            print(f"An error occurred: {e}")
            break
