# Jenkins Gradle Repository

This repository contains a basic **Jenkins Declarative Pipeline** for building and testing a Gradle-based application.

It is designed as a minimal, production-style starting point that can be extended with additional stages such as static analysis, security scans, Docker build, or deployment.

---

## 📌 Repository Structure

```
.
├── Jenkinsfile
├── build.gradle / build.gradle.kts
├── gradlew
├── gradlew.bat
├── gradle/
└── src/
```

---

## ⚙️ Jenkinsfile Overview

The pipeline is written using **Declarative Pipeline syntax** and performs the following steps:

### 1️⃣ Agent

```groovy
agent any
```

* Uses any available Jenkins agent (node/container).
* Can be restricted later using labels or Docker agents.

---

### 2️⃣ Stages

#### 🔹 Clean Workspace

```groovy
deleteDir()
```

* Deletes all files from the current workspace.
* Ensures a clean build environment.
* Prevents issues caused by leftover artifacts from previous builds.

---

#### 🔹 Checkout

```groovy
checkout scm
```

* Checks out source code from the configured SCM (Git, GitHub, etc.).
* Uses Jenkins job SCM configuration.

---

#### 🔹 Build & Test

```groovy
chmod +x gradlew
./gradlew clean build
```

* Makes Gradle wrapper executable.
* Runs:

  * `clean` → Removes previous build artifacts.
  * `build` → Compiles, runs tests, and packages the application.

If tests fail → Pipeline fails automatically.

---

### 3️⃣ Post Actions

```groovy
post {
    success {
        echo 'Build successful!'
    }
    failure {
        echo 'Build failed!'
    }
}
```

* On success → Logs success message.
* On failure → Logs failure message.
* Can be extended to:

  * Send email notifications
  * Trigger Slack alerts
  * Archive artifacts
  * Publish test reports

---

## 🚀 How to Use This Repository

### Step 1: Install Jenkins

You can run Jenkins using Docker:

```bash
docker run -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

Access Jenkins:

```
http://localhost:8080
```

---

### Step 2: Create a Pipeline Job

1. Go to **New Item**

2. Select **Pipeline**

3. Under **Pipeline Definition**

   * Choose: `Pipeline script from SCM`
   * SCM: `Git`
   * Repository URL: `<your-repo-url>`
   * Script Path: `Jenkinsfile`

4. Save and Build.

---

## 🔎 Pipeline Flow

```
Clean Workspace
        ↓
Checkout Code
        ↓
Gradle Build
        ↓
Run Tests
        ↓
Success / Failure Message
```

---

## 🧩 Requirements

* Jenkins 2.x+
* Java installed on agent
* Gradle wrapper included in repo
* Git configured in Jenkins

---

## 📈 Recommended Enhancements (Next Level)

You can enhance this pipeline with:

* ✅ Test report publishing (`junit`)
* ✅ Code coverage (JaCoCo)
* ✅ SonarQube scan
* ✅ Docker image build & push
* ✅ Multi-branch pipeline
* ✅ Parallel stages
* ✅ Build parameters
* ✅ Environment-specific deployments

---

## 🛠 Example: Add JUnit Reports

```groovy
post {
    always {
        junit 'build/test-results/test/*.xml'
    }
}
```

---

## 🧠 Best Practices

* Use Gradle Wrapper instead of system Gradle.
* Keep Jenkinsfile in repository (Pipeline as Code).
* Use multi-branch pipelines for feature branches.
* Avoid hardcoded credentials (use Jenkins Credentials store).
* Use agents with proper labels in production.

---

## 📌 Current Pipeline Scope

✔ Cleans workspace
✔ Checks out source code
✔ Builds application
✔ Runs unit tests
✔ Logs build status

This is a foundational CI pipeline suitable for:

* Java/Gradle applications
* Interview demonstrations
* CI learning setups
* Small internal services

---
