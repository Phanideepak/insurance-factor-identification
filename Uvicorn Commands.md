### **Uvicorn Commands**

Uvicorn is an ASGI server implementation for Python, typically used to serve FastAPI applications. Below is a list of common Uvicorn commands and their explanations.

---

### **1. Basic Uvicorn Command**

#### Command:
```bash
uvicorn main:app
```
- **Explanation**: This command runs the FastAPI app located in the `main.py` file with the `app` object.
  - `main`: Refers to the Python module (file) where the FastAPI application instance is located (`main.py`).
  - `app`: The FastAPI app instance.

---

### **2. Running with Reload Option**

#### Command:
```bash
uvicorn main:app --reload
```
- **Explanation**: The `--reload` flag makes Uvicorn restart the server whenever changes are detected in the code, which is useful during development.
- This command is equivalent to `python -m uvicorn main:app --reload`.

---

### **3. Specifying Host and Port**

#### Command:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
- **Explanation**: By default, Uvicorn runs on `127.0.0.1` (localhost) and port `8000`. To make the server accessible externally or on a different port:
  - `--host`: Specifies the IP address to bind to (e.g., `0.0.0.0` for all network interfaces).
  - `--port`: Specifies the port number (default is `8000`).

---

### **4. Running Uvicorn in Workers Mode (Multiprocessing)**

#### Command:
```bash
uvicorn main:app --workers 4
```
- **Explanation**: The `--workers` flag allows you to run multiple worker processes, which is useful for handling high traffic.
  - `--workers 4`: Runs 4 worker processes.
- This command is generally used in production for better performance.

---

### **5. Running with Custom Configurations (Using `--config`)**

#### Command:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --workers 4
```
- **Explanation**: Combines several options into a single command for custom configurations like reloading, worker processes, host, and port.

---

### **6. Specifying the ASGI Application Object**

#### Command:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --workers 4
```
- **Explanation**: You can specify the ASGI application object by appending `:app` after the module name.
  - If your FastAPI application is in `main.py` and the FastAPI app instance is `app`, you use `main:app`.

---

### **7. Running Uvicorn in HTTP/2 Mode**

#### Command:
```bash
uvicorn main:app --http2
```
- **Explanation**: Enables HTTP/2 support, which is beneficial for faster loading times and multiplexing for requests.
- Note that HTTP/2 support may require additional configuration or libraries depending on your operating system and Uvicorn version.

---

### **8. Setting Log Level**

#### Command:
```bash
uvicorn main:app --log-level debug
```
- **Explanation**: The `--log-level` option controls the level of logs output.
  - Options include:
    - `debug` (default for development)
    - `info` (default for production)
    - `warning`
    - `error`
    - `critical`

---

### **9. Enabling Access Logs**

#### Command:
```bash
uvicorn main:app --access-log
```
- **Explanation**: Enables access logs, which log every request that the server processes.
  - The logs contain useful information such as the request method, status code, IP address, and response time.

---

### **10. Specifying a Custom SSL Certificate (HTTPS)**

#### Command:
```bash
uvicorn main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```
- **Explanation**: For running the FastAPI app over HTTPS:
  - `--ssl-keyfile`: Specifies the path to the SSL private key file.
  - `--ssl-certfile`: Specifies the path to the SSL certificate file.
- This is useful for running the server in a secure, production environment.

---

### **11. Running Uvicorn as a Daemon (Background)**

#### Command:
```bash
uvicorn main:app --daemon
```
- **Explanation**: The `--daemon` option runs Uvicorn in the background as a daemon, which is useful for running production servers.

---

### **12. Using Uvicorn with Gunicorn (for Production)**

#### Command:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```
- **Explanation**: Gunicorn is a WSGI server that works with Uvicorn. It is commonly used in production environments.
  - `-w 4`: Specifies the number of worker processes (e.g., 4 workers).
  - `-k uvicorn.workers.UvicornWorker`: Uses Uvicorn as the worker class.
  - `main:app`: The module and FastAPI app object.

---

### **13. Running Uvicorn with Docker**

In a Dockerized environment, you can run Uvicorn with the following command in your `Dockerfile`:

#### Dockerfile Example:
```Dockerfile
FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

- **Explanation**: This Dockerfile sets up a Python 3.9 environment, installs dependencies, and runs Uvicorn in the container on port 80.

---

### **14. Viewing Uvicorn Help (List of Commands and Options)**

#### Command:
```bash
uvicorn --help
```
- **Explanation**: Displays a list of available options and arguments for running Uvicorn, including host, port, workers, logging levels, and more.

---

### **Summary Table of Common Uvicorn Commands**

| **Command**                                   | **Description**                                                   |
|-----------------------------------------------|-------------------------------------------------------------------|
| `uvicorn main:app`                            | Runs the FastAPI app in the `main.py` file.                       |
| `uvicorn main:app --reload`                   | Runs the app with hot reloading enabled.                          |
| `uvicorn main:app --host 0.0.0.0 --port 8000` | Binds Uvicorn to all IPs and port 8000.                           |
| `uvicorn main:app --workers 4`                | Runs the app with 4 worker processes.                             |
| `uvicorn main:app --http2`                    | Enables HTTP/2 support for faster responses.                      |
| `uvicorn main:app --log-level debug`          | Sets the log level to debug.                                      |
| `uvicorn main:app --access-log`               | Enables access logging for HTTP requests.                         |
| `uvicorn main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem` | Runs the server with HTTPS using specified SSL certificates. |
| `uvicorn main:app --daemon`                   | Runs the server as a background process (daemon).                 |
| `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app` | Runs Uvicorn with Gunicorn in production.                      |

---

These commands will help you manage your FastAPI app deployment with Uvicorn in different scenarios.