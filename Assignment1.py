import google.generativeai as genai
import os
import time
import json

api_key = "AIzaSyDdsDG7UGuxVprcKfIbB4b5nrEkcBTCHEk"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def process_prompts(input_file, output_file):
    results = []
    
    with open(input_file, 'r') as file:
        prompts = file.readlines()
    
    for prompt in prompts:
        prompt = prompt.strip()
        if not prompt:
            continue
        
        
        time_sent = int(time.time())
        
        response = model.generate_content(prompt)
        
       
        time_recvd = int(time.time())
        
        result = {
            "Prompt": prompt,
            "Message": response.text,
            "TimeSent": time_sent,
            "TimeRecvd": time_recvd,
            "Source": "Gemma"
        }
        
        results.append(result)
    
    
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)


process_prompts('input.txt', 'output.json')
