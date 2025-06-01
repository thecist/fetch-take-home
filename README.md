## Project Overview

This is a FastAPI-based receipt reward system with built-in testing and automatic scoring logic.

---

## Development Setup

**Requirements:**

* VSCode (with [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers))
  OR GitHub Codespaces
* No global Python or package setup needed

### How to Start the App

1. **Open in VSCode** (locally or in Codespace)
2. VSCode will automatically prompt to "Reopen in Container" using the `.devcontainer` setup
3. The API will start automatically in a terminal shell inside the container

> **If no prompt after extension installation:**

Open the VS Code command palette
(usually `Ctrl+Shift+P` or `Cmd+Shift+P` on Mac) and run:
`>Dev Containers: Rebuild Without Cache and Reopen in Container`

```bash

> **If the terminal running the API is accidentally closed:**

```bash
cd /app/src
python -m py_api
```

That will re-launch the FastAPI server using `uvicorn`.

---

## Running Tests

From inside the container:

```bash
cd /app/src
pytest
```

> `pytest` is pre-installed and configured
> Tests include **unit tests** and **integration tests**
> `PYTHONPATH` and relative imports are already handled

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

My current submission(with hash)
will be in python, but during the review time, I will be working on a replica
using JavaScript. The structure will be similar with the ony diffence being you
will need to add `RUNTIME=js` to the `.env` file to run the JavaScript version

Python's FastAPI was the best choice for this project