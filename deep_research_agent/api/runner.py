import subprocess
import sys


def start():
    """
    Starts the Uvicorn server using a subprocess.
    """
    try:
        print("Attempting to start Uvicorn server...")
        subprocess.run(
            [
                "uvicorn",
                "deep_research_agent.api.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
            ],
            check=True,
        )
    except FileNotFoundError:
        print(
            "Error: 'uvicorn' command not found. "
            "Make sure you have installed the API dependencies with 'uv sync --all-groups'.",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running Uvicorn: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    start()
