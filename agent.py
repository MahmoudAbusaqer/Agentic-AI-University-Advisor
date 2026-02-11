"""
MSU Registration Assistant Agent
Uses Claude API to answer student registration questions
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MSURegistrationAgent:
    def __init__(self, knowledge_base_path="knowledge_base.txt"):
        """Initialize the agent with Claude API"""
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        self.conversation_history = []
        
    def _load_knowledge_base(self, path):
        """Load the knowledge base from file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Warning: {path} not found. Run data_collector.py first!")
            return ""
    
    def create_system_prompt(self):
        """Create the system prompt for the agent"""
        return f"""You are a helpful academic advisor assistant for Missouri State University (MSU). 
Your role is to help students with course registration questions.

CRITICAL RULES - FOLLOW STRICTLY:

1. ACCURACY FIRST:
   - ONLY provide information that is explicitly stated in the knowledge base below
   - If information is not in the knowledge base, you MUST say "I don't know" and direct them to the appropriate office
   - NEVER guess, assume, or make up information
   - NEVER add information from your training data that isn't in the knowledge base

2. WHEN YOU DON'T KNOW:
   - Be honest: "I don't have specific information about that in my knowledge base."
   - Direct to appropriate contact:
     * General registration: Office of the Registrar (Registrar@MissouriState.edu, 417-836-5520)
     * Advising: Academic Advising and Transfer Center (Advise@MissouriState.edu, 417-836-5258)
     * Specific departments: Suggest contacting the relevant department

3. HANDLING VISUAL CONTENT:
   - When the knowledge base references images, screenshots, or videos:
     a) Extract and describe the steps in clear, numbered text format
     b) If the visual is complex and essential, say: "This involves a visual guide. For the complete step-by-step with screenshots, please visit: [URL]"
   - Never say "look at the image" - always convert to text instructions

4. RESPONSE FORMAT:
   - Start with a direct answer (if you know it)
   - Provide step-by-step instructions when applicable
   - Include relevant contact information
   - Cite the source page when appropriate
   - Keep responses clear and concise

5. BOUNDARIES:
   - Only answer questions about MSU course registration, enrollment, advising, and related academic policies
   - For financial aid, housing, or other non-registration topics, direct to appropriate offices
   - For specific course content or professor questions, direct to the department

KNOWLEDGE BASE:
{self.knowledge_base}

Remember: It's better to say "I don't know, please contact [office]" than to provide incorrect information.
"""

    def ask(self, question, stream=False):
        """
        Ask the agent a question

        Args:
            question: The student's question
            stream: Whether to stream the response

        Returns:
            The agent's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": question
        })

        # Call Claude API
        if stream:
            return self._stream_response()
        else:
            return self._get_response()

    def _get_response(self):
        """Get a complete response from Claude"""
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",  # Latest Sonnet model
                max_tokens=1000,
                system=self.create_system_prompt(),
                messages=self.conversation_history
            )

            # Extract the text response
            assistant_message = response.content[0].text

            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except Exception as e:
            return f"Error: {str(e)}\n\nPlease check your API key and internet connection."

    def _stream_response(self):
        """Stream response from Claude (for real-time output)"""
        try:
            full_response = ""

            with self.client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=self.create_system_prompt(),
                messages=self.conversation_history
            ) as stream:
                for text in stream.text_stream:
                    print(text, end="", flush=True)
                    full_response += text

            print()  # New line after streaming

            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": full_response
            })

            return full_response

        except Exception as e:
            error_msg = f"Error: {str(e)}\n\nPlease check your API key and internet connection."
            print(error_msg)
            return error_msg

    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []


def main():
    """Run the agent in terminal mode for testing"""
    print("=" * 80)
    print("MSU Course Registration Assistant")
    print("=" * 80)
    print("\nInitializing agent...\n")

    agent = MSURegistrationAgent()

    print("Agent ready! Ask me anything about course registration at Missouri State.")
    print("Type 'quit' to exit, 'reset' to start a new conversation.\n")

    while True:
        try:
            question = input("\n🎓 You: ").strip()

            if question.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! Good luck with registration! 🐻")
                break

            if question.lower() == 'reset':
                agent.reset_conversation()
                print("\n✓ Conversation reset. Starting fresh!\n")
                continue

            if not question:
                continue

            print("\n🤖 Assistant: ", end="")
            agent.ask(question, stream=True)

        except KeyboardInterrupt:
            print("\n\nGoodbye! Good luck with registration! 🐻")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Continuing...\n")


if __name__ == "__main__":
    main()