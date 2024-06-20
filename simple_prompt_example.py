
import ollama

while True:
    message = {'role': 'user', 'content': input('>_ ')}
    response = ollama.chat(model='llama3', messages=[message])
    print(response['message']['content'])