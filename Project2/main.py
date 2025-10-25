import tinytroupe
from tinytroupe.examples import create_lisa_the_data_scientist
from tinytroupe.factory import TinyPersonFactory
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    print("Hello from project2!")
    print("\n" + "="*50)
    print("Creating Lisa the Data Scientist...")
    print("="*50 + "\n")

    lisa = create_lisa_the_data_scientist()
    lisa.listen_and_act("Tell me about your life.")

    print("\n" + "="*50)
    print("Creating a custom Brazilian doctor...")
    print("="*50 + "\n")

    factory = TinyPersonFactory(context="A hospital in São Paulo.")
    person = factory.generate_person("Create a Brazilian person that is a doctor, likes pets and nature and loves heavy metal.")

    print("\n" + "="*50)
    print("Asking the doctor about their interests...")
    print("="*50 + "\n")

    person.listen_and_act("Tell me about your hobbies and interests.")


if __name__ == "__main__":
    main()
