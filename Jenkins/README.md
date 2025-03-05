In Jenkins, both Declarative and Scripted Pipelines are ways to define continuous delivery pipelines as code. 

### Declarative Pipeline:

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                // Build steps here
            }
        }
        stage('Test') {
            steps {
                // Test steps here
            }
        }
        // Add more stages as needed
    }
    post {
        always {
            // Post-build actions here
        }
    }
}
```

### Scripted Pipeline:

```groovy
node {
    stage('Build') {
        // Build steps here
    }
    stage('Test') {
        // Test steps here
    }
    // Add more stages as needed
    post {
        always {
            // Post-build actions here
        }
    }
}
```
