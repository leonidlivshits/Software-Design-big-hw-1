from Infrastructure.di.container import Container
from UserInterface.ConsoleInterface import ConsoleInterface

def main():
    container = Container()
    ui = ConsoleInterface(container)
    ui.run()

if __name__ == "__main__":
    main()