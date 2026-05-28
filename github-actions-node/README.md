Below is a **clean, interview-ready `README.md`** you can directly copy into your repository.
It explains **each file** and **each GitHub Actions step** in simple terms, aligned with your goal of *learning GitHub Actions fundamentals*.

---

# Node.js Docker CI – GitHub Actions Learning Repo

This repository is a **minimal example** to learn how **GitHub Actions** works using:

* A simple Node.js HTTP application
* Docker for consistent runtime
* A basic CI pipeline with a smoke test

The focus is **clarity and correctness**, not production complexity.

---

## Repository Structure

```text
.
├── index.js
├── package.json
├── Dockerfile
├── .dockerignore
└── .github/
    └── workflows/
        └── docker-ci.yml
```

---

## 1. `index.js` – Application Code

```js
const http = require('http');

const port = 3000;

const server = http.createServer((req, res) => {
  res.end('Hello Node!\n');
});

server.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
```

### What this file does

* Creates a basic HTTP server using Node.js
* Listens on port **3000**
* Responds with `Hello Node!` to any request

### Why it is intentionally simple

* No CI logic
* No auto-exit
* Behaves like a **real long-running service**
* Suitable for Docker and future Kubernetes usage

---

## 2. `package.json` – Project Metadata

```json
{
  "name": "node-hello",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  }
}
```

### Key points

* Defines the project name and version
* `npm start` runs `index.js`
* No `build` script because this app does **not** need a build phase

### Interview tip

> Not all Node.js applications have a build step.
> CI must match the application type.

---

## 3. `Dockerfile` – Container Definition

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY index.js .

EXPOSE 3000

CMD ["node", "index.js"]
```

### Step-by-step explanation

| Line                           | Purpose                                       |
| ------------------------------ | --------------------------------------------- |
| `FROM node:20-alpine`          | Lightweight Node.js base image                |
| `WORKDIR /app`                 | Sets working directory inside container       |
| `COPY package*.json ./`        | Copies dependency files first (layer caching) |
| `RUN npm install --production` | Installs dependencies                         |
| `COPY index.js .`              | Copies application code                       |
| `EXPOSE 3000`                  | Documents the application port                |
| `CMD ["node", "index.js"]`     | Starts the server                             |

### Why Docker is used here

* Same runtime locally and in CI
* Eliminates “works on my machine” issues
* Standard practice in modern CI/CD pipelines

---

## 4. `.dockerignore` – Build Optimization

```dockerignore
node_modules
.git
.gitignore
Dockerfile
README.md
```

### Why this file matters

* Prevents unnecessary files from being copied into the image
* Reduces image size
* Speeds up Docker builds

### Interview note

> `.dockerignore` is as important as `.gitignore` in CI pipelines.

---

## 5. GitHub Actions Workflow

### File: `.github/workflows/docker-ci.yml`

```yaml
name: Simple Docker CI

on:
  push:

jobs:
  ci:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t node-hello .

      - name: Run container
        run: |
          docker run -d -p 3000:3000 --name app node-hello

      - name: Simple smoke test
        run: |
          sleep 5
          curl http://localhost:3000

      - name: Cleanup
        run: docker rm -f app
```

---

## 6. GitHub Actions – Step-by-Step Explanation

### Trigger

```yaml
on:
  push:
```

* Workflow runs on **every push**
* Simplest and most common trigger

---

### Job Definition

```yaml
jobs:
  ci:
    runs-on: ubuntu-latest
```

* Defines a job named `ci`
* Runs on a GitHub-hosted Linux runner

---

### Step 1: Checkout Code

```yaml
- uses: actions/checkout@v4
```

* Pulls repository code into the runner
* Required for Docker builds and scripts

---

### Step 2: Build Docker Image

```yaml
- name: Build Docker image
  run: docker build -t node-hello .
```

* Builds Docker image from `Dockerfile`
* Tags it as `node-hello`

---

### Step 3: Run Container

```yaml
docker run -d -p 3000:3000 --name app node-hello
```

* Runs container in detached mode
* Maps container port `3000` to host `3000`
* Names container `app` for easy cleanup

---

### Step 4: Simple Smoke Test

```yaml
sleep 5
curl http://localhost:3000
```

* Waits briefly for server startup
* Sends HTTP request to verify app is reachable
* If `curl` fails → job fails automatically

### Why this is acceptable here

* Goal is **learning**, not production hardening
* Easy to understand and explain

---

### Step 5: Cleanup

```yaml
docker rm -f app
```

* Stops and removes container
* Keeps CI runner clean

---

## 7. What This Pipeline Demonstrates

* GitHub Actions basics
* Job and step execution order
* Docker image build
* Running containers in CI
* Simple smoke testing
* Exit codes controlling pipeline success/failure

---

## 8. What Is Intentionally NOT Included (Yet)

| Feature       | Reason                         |
| ------------- | ------------------------------ |
| Caching       | Added later for optimization   |
| Secrets       | Not needed for learning basics |
| `needs`       | Single-job pipeline            |
| Image push    | CD responsibility              |
| Health checks | Production concern             |

---

## 9. Interview-Ready Summary (Memorize)

> “This pipeline demonstrates a simple CI flow where a Docker image is built, run, and smoke-tested using GitHub Actions. The focus is on understanding jobs, steps, and failure handling without over-engineering.”

---
