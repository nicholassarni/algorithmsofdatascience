import tinytroupe
from tinytroupe.examples import create_lisa_the_data_scientist

def main():
    print("Hello from project2!")
    print(f"TinyTroupe version: {tinytroupe.__version__}")

    lisa = create_lisa_the_data_scientist()
    lisa.listen_and_act("Tell me about your life.")


if __name__ == "__main__":
    main()
