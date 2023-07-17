import gradio as gr
import random
import time
import openai  
  
# 用你的OpenAI API密钥替换这里  
openai.api_type = "azure"
openai.api_base = "https://openai-tester.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = "3ae22688a9714f30a92980a0529d7b57"

# Define a list of keyword replacements  
replacements = [  
    ("OBS", "OS@1"),  
    ("SSG", "SG@1"), 
    ("DCP", "DP@1"),
    ("HSBC", "HC@1"),     
    # Add more replacements as needed  
]  

message_list = []

def clean_msg():
    message_list.clear()
    #debug
    #print ("message clean")

def replace_keywords(text):  
    for keyword, replacement in replacements:  
        text = text.replace(keyword, replacement)  
    return text  
      
def revert_keywords(text):  
    for keyword, replacement in replacements:  
        text = text.replace(replacement, keyword)  
    return text       
      
def chat(chat_message,chat_history,engine_type):  
        
    # Replace keywords in user input  
    processed_message = replace_keywords(chat_message)  
    
    #debug
    #print(message_list)
    
    if chat_history is None:
        chat_history = []
    #    message_list = []

    if engine_type is None:
        engine_type = "gpt-35-turbo"
    else:
        engine_type = engine_type
    # append message to API
    message_list.append({"role": "user", "content": processed_message}); 
    
    # Call OpenAI's ChatCompletion API  
    response = openai.ChatCompletion.create(  
        engine=engine_type,  
        messages=message_list,  
        temperature=0.7,  
        max_tokens=800,  
        top_p=1,  
        frequency_penalty=0,  
        presence_penalty=0  
    )   
  
    # Extract the AI's response  
    ai_response = revert_keywords(response.choices[0].message["content"].strip())  
    # Reverd keyword in user input  
    #processed_response = revert_keywords(ai_response)  
    
    
    message_list.append({"role": "assistant", "content": ai_response})
    chat_history.append((processed_message.strip(), ai_response))  
    
    return "",chat_history,engine_type


with gr.Blocks() as demo:
    gr.Markdown(
    """
    # AI Chat Mask (OBS)
    A simple chatbot with masking using OpenAI's ChatCompletion API for OBS.
    """) 
    theme = "gradio/monochrome"
    title = "AI CHAT Mask (OBS)"
    engine_type = gr.Dropdown(  
    ["gpt-35-turbo", "gpt-4", "gpt-4-32k"], label="Engine", info="Select the Engine") 
    chatbot = gr.Chatbot(label="AI Chatbot")
    msg = gr.Textbox(label="Please input the query here: (Shift+Enter: to input new line)")
    state = gr.State()
    clear = gr.ClearButton([msg,chatbot,state])  
    
    msg.submit(chat, [msg, chatbot,engine_type], [msg, chatbot,engine_type])
    clear.click(clean_msg)


demo.launch(share=True)

