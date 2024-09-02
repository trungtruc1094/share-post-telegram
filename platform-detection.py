import platform
import os

def detect_system():
    system = platform.system()
    architecture = platform.machine()

    if system == "Darwin":
        if architecture == "arm64":
            print("You are running the script on a Mac with M1 (Apple Silicon).")
        else:
            print("You are running the script on a Mac with Intel architecture.")
    elif system == "Windows":
        print("You are running the script on a Windows PC.")
    else:
        print(f"You are running the script on {system} with {architecture} architecture.")

    return system, architecture

if __name__ == "__main__":
    detect_system()