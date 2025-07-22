import docker

def run_python_code(code: str) -> str:
    """
    Runs python code in a docker container and returns the output.
    """
    try:
        client = docker.from_env()
        client.ping()
    except docker.errors.DockerException:
        return "Error: Docker daemon is not running or not accessible. Please start Docker and try again."
    
    try:
        container = client.containers.run(
            "python:3.12-slim",
            command=["python", "-c", code],
            remove=True,
            stderr=True,
            stdout=True,
        )
        return container.decode("utf-8")
    except docker.errors.ContainerError as e:
        return e.stderr.decode("utf-8")
    except docker.errors.ImageNotFound:
        return "Error: python:3.12-slim image not found. Please pull it."
    except Exception as e:
        return f"An unexpected error occurred: {e}"