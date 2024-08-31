import google.generativeai as genai
import os
import time
import json

genai.configure(api_key="AIzaSyDdsDG7UGuxVprcKfIbB4b5nrEkcBTCHEk")
model = genai.GenerativeModel("gemini-1.5-flash")

def process_prompts(input_file, client_id, output_file):
    results = []
    file = open(input_file, 'r')
    prompts = file.readlines()
    file.close()

    for prompt in prompts:
        prompt = prompt.strip()

        if len(prompt) > 0:
            time_sent = int(time.time())
            response = model.generate_content(prompt)
            time_recvd = int(time.time())

            result = {
                "Prompt": prompt,
                "Message": response.text,
                "TimeSent": time_sent,
                "TimeRecvd": time_recvd,
                "Source": "Gemma",
                "ClientID": client_id
            }
            results.append(result)

    file = open(output_file, 'w')
    json.dump(results, file, indent=4)
    file.close()

def split_prompts(input_file, num_clients):
    file = open(input_file, 'r')
    prompts = file.readlines()
    file.close()

    prompts_per_client = len(prompts) // num_clients

    for i in range(num_clients):
        client_prompts = []
        start_index = i * prompts_per_client
        end_index = start_index + prompts_per_client

        for j in range(start_index, end_index):
            if j < len(prompts):
                client_prompts.append(prompts[j])

        client_id = "client_" + str(i + 1)
        client_prompt_file = "client_" + str(i + 1) + "_prompts.txt"

        client_file = open(client_prompt_file, 'w')
        for prompt in client_prompts:
            client_file.write(prompt)
        client_file.close()

        output_file = "output_" + client_id + ".json"
        process_prompts(client_prompt_file, client_id, output_file)

num_clients = 3

split_prompts('input.txt', num_clients)
