"""
Web Interface for MSU Registration Assistant
Flask app with simple chat interface
"""

from flask import Flask, render_template, request, jsonify, session
from agent import MSURegistrationAgent
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store agents per session
agents = {}

def get_agent():
    """Get or create agent for current session"""
    session_id = session.get('session_id')
    
    if not session_id:
        session_id = secrets.token_hex(8)
        session['session_id'] = session_id
    
    if session_id not in agents:
        agents[session_id] = MSURegistrationAgent()
    
    return agents[session_id]

@app.route('/')
def index():
    """Render the chat interface"""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """Handle question from user"""
    try:
        data = request.json
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Please enter a question'}), 400
        
        agent = get_agent()
        response = agent.ask(question)
        
        return jsonify({
            'question': question,
            'response': response
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset():
    """Reset conversation"""
    try:
        agent = get_agent()
        agent.reset_conversation()
        return jsonify({'message': 'Conversation reset'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("MSU Registration Assistant - Web Interface")
    print("=" * 80)
    print("\nStarting server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, port=5000)
