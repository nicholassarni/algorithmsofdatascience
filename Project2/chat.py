import tinytroupe
from tinytroupe.examples import create_lisa_the_data_scientist
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    print("=" * 50)
    print("Chat with Lisa the Data Scientist")
    print("=" * 50)
    print("Type 'quit' or 'exit' to end the conversation\n")

    # Create Lisa
    lisa = create_lisa_the_data_scientist()

    # Interactive chat loop
    while True:
        # Get user input
        user_input = input("You: ")

        # Check if user wants to exit
        if user_input.lower() in ['quit', 'exit']:
            print("\nGoodbye!")
            break

        # Skip empty inputs
        if not user_input.strip():
            continue

        # Lisa responds
        print()
        lisa.listen_and_act(user_input)
        print()

if __name__ == "__main__":
    main()
