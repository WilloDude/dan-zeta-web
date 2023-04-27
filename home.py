from flask import Flask, request, jsonify
import openai
import json

# Initialize Flask app
app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = "YOUR_API_KEY"

# Set up GPT-2 model
model_engine = "davinci"  # Change this to a different GPT-2 model if desired
model = openai.Completion.create(engine=model_engine)

# Define function to generate a response from GPT-2
def generate_response(prompt):
    prompt_text = prompt + "\nAI:"
    response = model.generate(
        prompt=prompt_text,
        temperature=0.7,
        max_tokens=100,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
    )
    message = response.choices[0].text.strip().replace("AI:", "")
    return message

# Define route for chatbot interface
@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.form['prompt']
    message = generate_response(prompt)
    return jsonify({'response': message})

# Define home page with HTML form for chatbot
@app.route('/')
def home():
    return '''
        <html>
            <head>
                <title>Chatbot Demo</title>
            </head>
            <body>
                <h1>Welcome to the Chatbot Demo</h1>
                <form method="post" action="/chat">
                    <input type="text" name="prompt" id="prompt" placeholder="Ask a question...">
                    <input type="submit" value="Send">
                </form>
                <div id="response"></div>
                <script>
                    // Send form data to server and display response
                    const form = document.querySelector('form');
                    form.addEventListener('submit', async (e) => {
                        e.preventDefault();
                        const prompt = document.querySelector('#prompt').value;
                        const responseDiv = document.querySelector('#response');
                        const response = await fetch('/chat', {
                            method: 'POST',
                            body: new FormData(form)
                        }).then(response => response.json());
                        responseDiv.innerHTML += '<p>You: ' + prompt + '</p>';
                        responseDiv.innerHTML += '<p>Bot: ' + response['response'] + '</p>';
                        document.querySelector('#prompt').value = '';
                    });
                </script>
            </body>
        </html>
    '''

# Run Flask app
if __name__ == '__main__':
    app.run()
