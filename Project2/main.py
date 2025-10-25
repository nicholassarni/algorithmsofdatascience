import tinytroupe
from tinytroupe.examples import create_lisa_the_data_scientist
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    print("Hello from project2!")

    lisa = create_lisa_the_data_scientist()
    lisa.listen_and_act("Tell me about your life.")


if __name__ == "__main__":
    main()
