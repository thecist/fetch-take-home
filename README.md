## Project Overview

This is a completion of Fetch's take home assessment, given on 5/29/2025.

---

## Development Setup

## Option 1: Using Local DevContainer (Preferred for VS Code)

> **Best for:** Clean setup with VS Code and Docker.

### Prerequisites

* [Docker](https://www.docker.com/products/docker-desktop) installed
* [Visual Studio Code](https://code.visualstudio.com/)
* [Dev Containers
  extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
* Do not use `git bash for windows` on Windows, use Powershell(uvicorn acts weird
  if it thinks it is running on a Linux system on Windows)

### Steps

1. **Open the project in VS Code**
   * Either `code .` from the root folder or open manually.

2. **Reopen in Dev Container**
   * You'll get a prompt like:
     > *“Dev container configuration found. Reopen in container?”*
   * Click **“Reopen in Container”**.
   * If you don't see the prompt, open the command palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on Mac) and run:
      > `Dev Containers: Rebuild Without Cache and Reopen in Container`

3. **It will automatically:**

   * Build the container
   * Install Python + JS dependencies
   * Run the `start.sh` to launch either FastAPI or Node API

---

## Option 2: Local Virtual Environment (No Docker)

> **Best for:** Lightweight development or if Docker/Codespaces aren't working.

### Prerequisites

* Python 3.10+
* Node.js (only if you want to run JS version)

### Python-only Setup

1. **Navigate to the project root**

   ```bash
   cd /path/to/fetch-take-home
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv .venv
   ```

3. **Activate it**

   * On **Linux/macOS**:

     ```bash
     source .venv/bin/activate
     ```
   * On **Windows**:

     ```cmd
     .venv\Scripts\activate
     ```

4. **Install Python dependencies**

   ```bash
   cd src
   python -m pip install -r py_api/requirements-dev.txt
   ```

5. **Run the FastAPI app**

   ```bash
   python -m py_api
   ```

   > This will use `__main__` from `app.py` to launch the API.

---

## Running Tests

From the `src` directory:

```bash
pytest
```

---

## Production Setup

All you need is Docker and Docker Compose.

From the **project root** (e.g. `fetch-take-home/`), run:

```bash
docker compose up --build
```

> This will:
>
> * Build the FastAPI app
> * Launch it on port `3000`
> * Use the production-ready image and environment

---

## Notes

* API docs will be available at [http://localhost:3000/docs](http://localhost:3000/docs)
* If you make changes to the code, the server automatically restarts (in dev) or re-run `docker compose up` (in prod) to reflect updates
* API is built with clear OpenAPI descriptions and is easily testable via Swagger UI

---

## To Reviewer
I have recently fallen in love with the almost too perfect mix of FastAPI,
Pydantic, Swagger, and OpenAPI. Sadly, I am not familiar enough with python to
survive a 5 hours collboarative coding session.

My current submission(with hash) will be in python as it is the best choice
considering the assessment requirements, but during the review time, I will be
working on a replica using JavaScript(the language I am most familiar with). The
structure will be similar with the ony diffence being you will need to add
`RUNTIME=js` to the `.env` file to run the JavaScript version. The purpose of
the rewrite is to both showcase my JavaScript skills and provide a more familiar
codebase for us to work on together during the next stage.