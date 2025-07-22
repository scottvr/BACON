# 1. Use a minimal, trusted base image
FROM python:3.11-slim

# 2. Create a non-root user for execution
RUN useradd --create-home --shell /bin/bash appuser

# 3. Create a working directory
WORKDIR /app

# 4. Pre-install common, trusted libraries.
# This avoids needing network access in the container.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Switch to the non-root user
USER appuser

# 6. Set the default command
CMD ["python", "main.py"]
