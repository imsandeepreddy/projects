# GitHub Actions Self-Hosted Runner in Docker

This repository provides a Docker-based self-hosted GitHub Actions runner. The runner is built on an Ubuntu container and includes necessary dependencies for running GitHub Actions workflows.

## 🚀 Features
- Runs a self-hosted GitHub Actions runner inside a Docker container.
- Uses a non-root user for security.
- Automatically configures and starts the runner.
- Installs required dependencies, including `libicu-dev` for .NET compatibility.

## 🛠️ Setup & Installation

### 1️⃣ Build the Docker Image
```sh
docker build -t github-runner .
```

### 2️⃣ Run the Container
Replace `YOUR_ORG/YOUR_REPO` with your actual GitHub organization and repository details.
```sh
docker run -d \
   --name actions-runner \
   --restart always \
   -e REPO_URL="https://github.com/YOUR_ORG/YOUR_REPO" \
   -e RUNNER_TOKEN="NEW_TOKEN_HERE" \
   github-runner
```

### 3️⃣ Verify the Runner in GitHub
Go to **GitHub Repository Settings > Actions > Runners** and check if the runner appears online.

## 📝 Dockerfile Explanation
```dockerfile
FROM ubuntu:latest

# Install dependencies
RUN apt update && apt install -y \
    curl jq git sudo \
    libicu-dev \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN useradd -m runner && echo "runner ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/runner

# Switch to non-root user
USER runner
WORKDIR /home/runner

USER root
COPY entrypoint.sh /home/runner/entrypoint.sh
RUN chmod +x /home/runner/entrypoint.sh && chown runner:runner /home/runner/entrypoint.sh

USER runner
RUN curl -o actions-runner-linux-x64-2.322.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.322.0/actions-runner-linux-x64-2.322.0.tar.gz
RUN echo "b13b784808359f31bc79b08a191f5f83757852957dd8fe3dbfcc38202ccf5768  actions-runner-linux-x64-2.322.0.tar.gz" | shasum -a 256 -c
RUN tar xzf ./actions-runner-linux-x64-2.322.0.tar.gz
WORKDIR /home/runner

# Default command to start the runner
CMD ["/home/runner/entrypoint.sh"]
```
### Key Points:
- Installs necessary dependencies (`libicu-dev` for .NET support).
- Creates a non-root `runner` user.
- Downloads and extracts the GitHub Actions runner binary.
- Copies the `entrypoint.sh` script and sets it as the default command.

## 📜 Entrypoint Script (`entrypoint.sh`)
```bash
#!/bin/bash
set -e

# Check if the runner is already configured
if [ ! -f .runner ]; then
    echo "Configuring GitHub Actions Runner..."
    ./config.sh --url $REPO_URL --token $RUNNER_TOKEN --unattended --replace
fi

echo "Starting GitHub Actions Runner..."
exec ./run.sh
```
### Key Points:
- Configures the GitHub Actions runner only if it's not already set up.
- Uses `exec ./run.sh` to properly start the runner.

## 📌 Stopping & Removing the Runner
To stop the runner container:
```sh
docker stop actions-runner
```
To remove the container:
```sh
docker rm actions-runner
```

## 🛠️ Debugging
Check logs if the runner is not appearing in GitHub:
```sh
docker logs actions-runner
```

Access the container shell:
```sh
docker exec -it actions-runner bash
```

## 📚 References
- [GitHub Actions Self-Hosted Runners](https://docs.github.com/en/actions/hosting-your-own-runners)
- [GitHub Actions Runner Releases](https://github.com/actions/runner/releases)

## 🎯 Conclusion
This setup allows you to run a self-hosted GitHub Actions runner inside a Docker container, providing flexibility and isolation. 🚀