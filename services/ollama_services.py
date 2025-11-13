import requests
import subprocess
import time
from typing import Tuple, Optional

def get_ollama_url(host: str = "http://localhost:11434", 
                   port: int = 11434,
                   auto_start: bool = True,
                   max_wait: int = 30) -> Tuple[Optional[str], bool, str]:
    """
    Get the Ollama server URL, starting it if necessary.
    
    Args:
        host: Default host URL to check/use
        port: Port number for the server
        auto_start: Whether to start the server if not running
        max_wait: Maximum seconds to wait for startup
    
    Returns:
        Tuple of (url: str or None, started: bool, message: str)
        - url: The server URL if running, None otherwise
        - started: True if we started the server, False if already running
        - message: Status message
    """
    url = f"http://localhost:{port}"
    
    # Check if already running
    try:
        response = requests.get(f"{url}/api/tags", timeout=2)
        if response.status_code == 200:
            return url, False, "Ollama server already running"
    except:
        pass
    
    # Not running - start it if requested
    if not auto_start:
        return None, False, "Ollama server not running"
    
    # Start the server
    try:
        process = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except FileNotFoundError:
        return None, False, "Ollama not installed"
    except Exception as e:
        return None, False, f"Failed to start: {str(e)}"
    
    # Wait for server to be ready
    start_time = time.time()
    while time.time() - start_time < max_wait:
        if process.poll() is not None:
            return None, False, "Process exited unexpectedly"
        
        try:
            response = requests.get(f"{url}/api/tags", timeout=2)
            if response.status_code == 200:
                elapsed = time.time() - start_time
                return url, True, f"Started in {elapsed:.1f}s"
        except:
            pass
        
        time.sleep(1)
    
    process.terminate()
    return None, False, f"Timeout after {max_wait}s"

def get_ollama_models_as_list():
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')[1:]  # Skip header
    # models = [line.split()[0].split(':')[0] for line in lines if line.strip()]
    models = [line.split()[0] for line in lines if line.strip()]
    return models

def get_available_models_my_version():
    models = []
    try:
        results = subprocess.run(['ollama', 'list'])

        x =  [line.split(' ')[0] for line in results.split('\n')]
        print(x)
        return x
        # lines = results.split('\n')
        # for line in lines[1:]:
        #     model = line.split(' ')[0]
        #     models.append(model)
        # return models
    except:
        return 'Error in geting available models from ollama'
    

# Example usage
if __name__ == "__main__":
    url, started, message = get_ollama_url()
    
    if url:
        print(f"✓ {message}")
        print(f"URL: {url}")
        if started:
            print("Note: Server started by this script")
    else:
        print(f"✗ {message}")