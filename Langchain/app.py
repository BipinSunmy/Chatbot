from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Import your chatbot model and get_response function
from Chatbot import get_response, load

@app.route('/')
def index():
    return render_template('Front.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = None
    url = None
    data = None
    
    if 'message' in request.form:
        message = request.form['message']
        
    if 'url' in request.form:
        url = request.form['url']
        data = load(url=url)
    
    # Ensure at least one input is provided
    if not message and not url:
        return jsonify({'response': 'No valid input received'})
    
    # Process the input with your model
    try:
        response = get_response(db=data, ques=message)
    except Exception as e:
        return jsonify({'response': f'Error processing request: {str(e)}'})
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
