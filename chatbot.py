import re

# Function to handle responses based on user input
def respond_to_query(query):
    # Convert the query to lowercase for case-insensitive matching
    query = query.lower()

    # Define response rules based on keywords or patterns
    if re.search(r'\bhello\b|\bhi\b', query):
        return "Hey there! How can I assist you today?"
    elif re.search(r'\bhow are you\b|\bhow\'s it going\b', query):
        return "I'm just a friendly bot doing great! How can I help you today?"
    elif re.search(r'\bwhat is your name\b|\bwho are you\b', query):
        return ("Hi! I'm PyBot-1.01, your friendly assistant. I can help with basic arithmetic and have a chat with you. 😊")
    elif re.search(r'\bbye\b|\bgoodbye\b', query):
        return "Goodbye! Have an amazing day! 🌟"
    elif re.search(r'\bweather\b', query):
        return "I can't check the weather for you, but I recommend using a weather app to get the latest updates."
    elif re.search(r'\bhelp\b', query):
        return "I'm here to help! You can ask me about greetings, my name, or even basic arithmetic operations."
    else:
        # Check for arithmetic operations
        return perform_arithmetic_operations(query)

def perform_arithmetic_operations(query):
    # Regular expressions to identify arithmetic operations
    match = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', query)

    if match:
        num1 = float(match.group(1))
        operator = match.group(2)
        num2 = float(match.group(3))

        # Perform the operation based on the operator
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                return "Oops! Division by zero isn't allowed. Please try another calculation."
        else:
            return "Hmm, that operation isn't supported. Can you try another one?"

        return f"The result of {num1} {operator} {num2} is {result}. Let me know if you need anything else!"
    else:
        return "Sorry, I didn't quite catch that. Could you please provide a clear arithmetic expression?"

# Main loop to interact with the user
def chatbot():
    print("Welcome to PyBot-1.01! Type 'bye' or 'goodbye' whenever you want to end our chat.")

    while True:
        try:
            user_input = input("You: ")

            # Check for exit condition
            if user_input.lower() in ['bye', 'goodbye']:
                print("Chatbot: Farewell! Have a fantastic day! 🌞")
                break

            # Get the chatbot's response
            response = respond_to_query(user_input)
            print(f"Chatbot: {response}")

        except Exception as e:
            print(f"Oh no! An error occurred: {e}")

# Run the chatbot
if __name__ == "__main__":
    chatbot()
