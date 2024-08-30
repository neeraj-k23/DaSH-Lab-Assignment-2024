import google.generativeai as genai
import os
import time
import json

# Configure the API key
api_key = "AIzaSyDdsDG7UGuxVprcKfIbB4b5nrEkcBTCHEk"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def process_prompts(input_file, client_id, output_file):
    results = []
    
    with open(input_file, 'r') as file:
        prompts = file.readlines()
    
    for prompt in prompts:
        prompt = prompt.strip()
        if not prompt:
            continue
        
        # Capture the time when the prompt is sent
        time_sent = int(time.time())
        
        # Generate response from the API
        response = model.generate_content(prompt)
        
        # Capture the time when the response is received
        time_recvd = int(time.time())
        
        # Assume response is valid. If the prompt-response pair is not valid, set "Source" to "user"
        # Implement any logic here if needed to check validity (e.g., matching prompt-response pairs)

        result = {
            "Prompt": prompt,
            "Message": response.text,
            "TimeSent": time_sent,
            "TimeRecvd": time_recvd,
            "Source": "Gemma",
            "ClientID": client_id
        }
        
        results.append(result)
    
    # Write the results to the output JSON file
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)

def split_prompts(input_file, num_clients):
    with open(input_file, 'r') as file:
        prompts = file.readlines()
    
    prompts_per_client = len(prompts) // num_clients
    for i in range(num_clients):
        client_prompts = prompts[i * prompts_per_client:(i + 1) * prompts_per_client]
        client_id = f"client_{i+1}"
        output_file = f"output_{client_id}.json"
        with open(f"client_{i+1}_prompts.txt", 'w') as client_file:
            client_file.writelines(client_prompts)
        process_prompts(f"client_{i+1}_prompts.txt", client_id, output_file)

# Number of clients to split prompts among
num_clients = 3  # Adjust as needed

# Call the function to split and process prompts
split_prompts('input.txt', num_clients)
