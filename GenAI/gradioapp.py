import gradio as gr
from openai import OpenAI

ashu_key = "sk-proj-"

client = OpenAI(api_key=ashu_key)

def chat_with_llm(message, history):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=message
    )
    return response.output_text

#gr.ChatInterface(fn=chat_with_llm).launch()
gr.ChatInterface(fn=chat_with_llm, type="messages").launch(server_name="0.0.0.0", server_port=7860)

