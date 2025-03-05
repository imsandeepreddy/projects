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