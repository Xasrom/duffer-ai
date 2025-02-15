from fastapi import FastAPI
import gradio as gr

# Create a FastAPI app
app = FastAPI()

# Define chatbot response logic
def chatbot_response(message):
    responses = {
        "hello": "Hey there! 😊 How can I assist you today?",
        "how are you": "I'm just a chatbot, but I'm feeling great! What about you?",
        "who made you": "I was built by Ritik, my master! 🚀",
        "bye": "Goodbye! Have a great day ahead! 👋",
    }
    return responses.get(message.lower(), "I'm not sure, but I'm happy to chat! 😊")

# Gradio UI for chatbot
def gradio_chat(message):
    return chatbot_response(message)

# Create Gradio interface
interface = gr.Interface(
    fn=gradio_chat,
    inputs="text",
    outputs="text",
    title="Duffer AI - Friendly Chatbot",
    description="Chat with Duffer AI - Your friendly assistant!",
)

# FastAPI endpoint for chatting
@app.get("/chat/{message}")
def chat(message: str):
    return {"response": chatbot_response(message)}

# Launch Gradio UI
@app.get("/")
def gradio_app():
    return interface.launch(share=True)
