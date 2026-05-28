# Stage 1: Build stage to download and isolate dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
# Install dependencies into a localized deployment directory
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime stage keeping the image size minimal
FROM python:3.11-slim AS runtime
WORKDIR /app

# Copy only the compiled packages from the builder stage
COPY --from=builder /root/.local /root/.local
# Copy your actual application source code files
COPY . .

# Update the system PATH environment variable to find the installed packages
ENV PATH=/root/.local/bin:$PATH

CMD ["python3", "app.py"]
