Below is a **one-page, interview-ready GitHub Actions cheat sheet**.
You can **read this before interviews** and confidently answer most CI/CD questions.

---

# GitHub Actions – One-Page Interview Cheat Sheet

---

## 1. What is GitHub Actions?

> GitHub Actions is a CI/CD platform that allows you to automate build, test, and deployment workflows directly from a GitHub repository using YAML files.

---

## 2. Core Building Blocks

### Workflow

* YAML file under `.github/workflows/`
* Triggered by events like `push`, `pull_request`, `schedule`

```yaml
on: push
```

---

### Job

* A set of steps executed on a runner
* Jobs run **in parallel by default**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
```

---

### Step

* Individual task inside a job
* Can be an **action** or a **shell command**

```yaml
- uses: actions/checkout@v4
- run: npm install
```

---

### Runner

* Machine that runs jobs
* Types:

  * GitHub-hosted (`ubuntu-latest`)
  * Self-hosted

---

## 3. Common Events (Triggers)

| Event               | Usage            |
| ------------------- | ---------------- |
| `push`              | Run on code push |
| `pull_request`      | Validate PRs     |
| `workflow_dispatch` | Manual trigger   |
| `schedule`          | Cron jobs        |

```yaml
on:
  pull_request:
```

---

## 4. Actions vs Commands

| Type    | Example                       |
| ------- | ----------------------------- |
| Action  | `uses: actions/setup-node@v4` |
| Command | `run: npm install`            |

---

## 5. Environment Variables

### Global

```yaml
env:
  NODE_ENV: production
```

### Step-level

```yaml
- run: echo $NODE_ENV
```

---

## 6. Secrets (Very Important)

* Stored in **Repo → Settings → Secrets**
* Automatically masked in logs
* Accessed via `${{ secrets.NAME }}`

```yaml
password: ${{ secrets.DOCKERHUB_TOKEN }}
```

**Interview line:**

> Secrets are injected at runtime and never stored in the repo.

---

## 7. `needs` (Job Dependencies)

* Controls execution order
* Enables output sharing

```yaml
test:
  needs: build
```

**Key point:**

> Without `needs`, jobs run in parallel.

---

## 8. Cache (Performance Optimization)

Used to speed up builds (e.g., npm, pip, Maven)

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('package-lock.json') }}
```

**Interview tip:**

> Cache restores before install, saves after job completion.

---

## 9. Exit Codes = Pipeline Result

* `exit 0` → success
* `exit 1` → failure
* Any failing command fails the job automatically

```yaml
- run: curl http://localhost:3000
```

---

## 10. Artifacts

Used to share files between jobs or download results

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: logs
    path: build.log
```

---

## 11. Matrix Builds

Run the same job with multiple versions

```yaml
strategy:
  matrix:
    node: [18, 20]
```

---

## 12. Docker in GitHub Actions

Common flow:

1. Build image
2. Run container
3. Smoke test
4. (Optional) Push image

```yaml
docker build -t app .
docker run -d -p 3000:3000 app
```

---

## 13. CI vs CD (Classic Interview Question)

| CI              | CD               |
| --------------- | ---------------- |
| Build & test    | Deploy           |
| Validate code   | Release software |
| Runs on PR/push | Runs on main/tag |

---

## 14. Common Interview Mistakes (Avoid These)

❌ Running long-running servers directly in CI
❌ Hard-coding secrets
❌ Overusing `sleep` in production pipelines
❌ Missing lock files (`package-lock.json`)

---

## 15. 30-Second Interview Answer (Memorize)

> “GitHub Actions lets us define CI/CD pipelines as code using YAML. A workflow is triggered by events, runs jobs on runners, and executes steps sequentially. We use secrets for sensitive data, cache for performance, and job dependencies with `needs` for controlled execution.”

---
Below is an **in-depth, interview-oriented explanation** of each topic, with **clear mental models, examples, and when-to-use guidance**.
This is written so you can **both understand and explain** under interview pressure.

---

# 1. `needs` vs Parallel Jobs

## Default behavior: Parallel jobs

By default, **all jobs run in parallel**.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
  test:
    runs-on: ubuntu-latest
```

### What happens

* `build` and `test` start at the same time
* No dependency or order guaranteed

### When parallel jobs are good

* Independent tasks
* Faster pipelines
* Examples:

  * Lint + unit tests
  * Multiple language builds
  * Matrix builds

---

## `needs`: Explicit dependency

```yaml
jobs:
  build:
    runs-on: ubuntu-latest

  test:
    needs: build
    runs-on: ubuntu-latest
```

### What `needs` does

* Enforces **execution order**
* `test` runs **only if `build` succeeds**
* Allows **sharing outputs**

---

## Sharing outputs with `needs`

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tag }}
    steps:
      - id: meta
        run: echo "tag=abc123" >> $GITHUB_OUTPUT

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying ${{ needs.build.outputs.image-tag }}"
```

---

## Interview-ready summary

| Concept        | Parallel Jobs | `needs`                 |
| -------------- | ------------- | ----------------------- |
| Execution      | Concurrent    | Sequential              |
| Dependency     | None          | Explicit                |
| Failure impact | Independent   | Downstream blocked      |
| Use case       | Speed         | Control & orchestration |

**Strong interview line:**

> “Jobs run in parallel by default; `needs` is used to model real pipeline stages and enforce correctness.”

---

# 2. Caching vs Docker Layer Cache

This is a **very common interview trap**.

---

## GitHub Actions Cache (`actions/cache`)

### Purpose

Caches **dependencies** between workflow runs.

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: npm-${{ hashFiles('package-lock.json') }}
```

### Characteristics

* Restored **before install**
* Saved **after job completes**
* Based on keys (hashes)

### Best for

* npm, pip, Maven, Gradle
* Speeds up CI execution

---

## Docker Layer Cache

### Purpose

Caches **Docker build layers**.

```dockerfile
COPY package.json .
RUN npm install
COPY . .
```

### How it works

* If a layer doesn’t change, Docker reuses it
* Cache invalidates **top-down**

### Best for

* Faster Docker builds
* Image creation speed

---

## Key difference (very important)

| Aspect    | Actions Cache | Docker Cache       |
| --------- | ------------- | ------------------ |
| Scope     | Workflow runs | Docker build       |
| Storage   | GitHub cache  | Docker daemon      |
| Key-based | Yes           | No (content-based) |
| Use case  | Dependencies  | Image layers       |

---

## Interview-ready line

> “GitHub cache optimizes workflow execution, Docker cache optimizes image builds. They solve different problems.”

---

# 3. Self-Hosted Runners

## What they are

Machines **you manage** that run GitHub Actions jobs.

```yaml
runs-on: self-hosted
```

---

## Why use self-hosted runners

### 1. Network access

* On-prem servers
* Private VPC
* Internal databases

### 2. Performance

* Larger CPU/RAM
* GPU workloads

### 3. Cost control

* Avoid GitHub-hosted minute limits

---

## Downsides (interviewers expect this)

* You manage:

  * OS patching
  * Security
  * Availability
* Can become single point of failure

---

## Typical real-world use cases

* Deploying to internal Kubernetes clusters
* Running Terraform against private clouds
* Legacy systems

---

## Interview-ready answer

> “Self-hosted runners are used when jobs need private network access, special hardware, or cost optimization.”

---

# 4. Environment Approvals

## What is an Environment?

A protected deployment target like:

* `dev`
* `staging`
* `prod`

Defined in **GitHub → Environments**

---

## Workflow example

```yaml
deploy:
  runs-on: ubuntu-latest
  environment: production
  steps:
    - run: echo "Deploying to prod"
```

---

## What environments provide

### 1. Manual approvals

* Require human approval before job runs

### 2. Environment-specific secrets

* Different secrets per environment

### 3. Deployment history

* Audit trail

---

## Real-world usage

* CI runs automatically
* CD to production requires approval

---

## Interview-ready line

> “Environments add governance to deployments by enforcing approvals and isolating secrets per environment.”

---

# 5. Rollback Strategies (Critical for Senior Roles)

## Rollback is NOT a GitHub Actions feature

GitHub Actions **enables** rollback strategies but does not define them.

---

## 1. Image-based rollback (most common)

### Strategy

* Deploy immutable versions (tags)
* Roll back by redeploying previous tag

```text
app:1.2.0 → app:1.1.3
```

### Why it works

* Deterministic
* Fast
* No rebuild required

---

## 2. Git-based rollback

### Strategy

* Revert commit
* Trigger pipeline again

```bash
git revert <commit>
git push
```

### Downsides

* Slower
* Changes history

---

## 3. Blue-Green deployment

### Strategy

* Two environments (blue & green)
* Switch traffic on success

### Rollback

* Switch traffic back

---

## 4. Canary deployment

### Strategy

* Deploy to small % of users
* Monitor metrics
* Gradually increase

### Rollback

* Stop rollout immediately

---

## Interview-ready summary

| Strategy       | Speed      | Safety    | Complexity |
| -------------- | ---------- | --------- | ---------- |
| Image rollback | Fast       | High      | Low        |
| Git revert     | Medium     | Medium    | Low        |
| Blue-green     | Fast       | Very high | Medium     |
| Canary         | Controlled | Very high | High       |

---

## 30-second senior-level answer (memorize)

> “In CI/CD, we rely on immutable artifacts and versioned deployments. Rollback is typically achieved by redeploying a previously known-good image rather than rebuilding or modifying code.”

---

