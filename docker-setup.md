If you'd like to use the official **Uvicorn Gunicorn FastAPI Docker image**, it simplifies the process by providing a pre-configured image tailored for FastAPI applications. Here's how you can dockerize your FastAPI app using it:

---

### 1. **Prepare Your FastAPI Application**
Ensure your application is structured properly:
```
app/
├── main.py          # Entry point for FastAPI application
├── requirements.txt # Dependencies (optional if using poetry/pipenv)
```

#### `main.py` Example:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Docker with Uvicorn!"}
```

---

### 2. **Create a `requirements.txt` File**
List all your dependencies:
```plaintext
fastapi
```

---

### 3. **Create a `Dockerfile`**
Use the official **Uvicorn Gunicorn FastAPI** image as the base.

#### Example Dockerfile:
```dockerfile
# Use the official Uvicorn Gunicorn FastAPI image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Set the working directory inside the container
WORKDIR /app

# Copy your FastAPI app and dependencies
COPY ./app /app
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the default port used by Uvicorn
EXPOSE 8000
```

---

### 4. **Build the Docker Image**
Run the following command in the directory with the `Dockerfile`:
```bash
docker build -t fastapi-uvicorn-app .
```

---

### 5. **Run the Docker Container**
Start the container:
```bash
docker run -d -p 8000:80 fastapi-uvicorn-app
```

- The container uses port **80** internally by default, which maps to your local port **8000** in this example.
- Access the app at [http://localhost:8000](http://localhost:8000).

---

### 6. **(Optional) Customize Uvicorn Configuration**
The `tiangolo/uvicorn-gunicorn-fastapi` image uses sensible defaults, but you can customize the behavior using environment variables or configuration files.

#### Add Custom Configurations
- **Environment Variables**:
  You can pass variables such as:
  ```bash
  docker run -d -p 8000:80 -e WORKERS_PER_CORE=2 -e MAX_WORKERS=4 fastapi-uvicorn-app
  ```
  - `WORKERS_PER_CORE`: Set the number of worker processes per CPU core.
  - `MAX_WORKERS`: Maximum number of workers.

- **Custom Command**:
  To override the default command in the `Dockerfile`:
  ```dockerfile
  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
  ```

---

### 7. **(Optional) Add a `docker-compose.yml` File**
For multi-service setups or easier management, use Docker Compose.

#### Example `docker-compose.yml`:
```yaml
version: "3.9"
services:
  app:
    image: fastapi-uvicorn-app
    build:
      context: .
    ports:
      - "8000:80"
    environment:
      WORKERS_PER_CORE: 2
      MAX_WORKERS: 4
```

Run:
```bash
docker-compose up -d
```

---