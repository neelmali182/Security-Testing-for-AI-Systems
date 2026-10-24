pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = 'aishield'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                bat 'py -3.11 -m venv .venv'
                bat '.venv\\Scripts\\python.exe -m pip install --upgrade pip'
                bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Automated and security tests') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pytest -q --junitxml=pytest-results.xml'
            }
            post {
                always {
                    junit testResults: 'pytest-results.xml', allowEmptyResults: true
                }
            }
        }

        stage('Build Docker image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%IMAGE_TAG% .'
            }
        }

        stage('Deploy demonstration app') {
            when {
                expression {
                    def currentBranch = env.BRANCH_NAME ?: env.GIT_BRANCH ?: ''
                    return currentBranch == 'main' || currentBranch.endsWith('/main')
                }
            }
            steps {
                bat 'docker rm -f aishield-app 2>NUL || exit /B 0'
                bat 'docker run -d --name aishield-app --restart unless-stopped -p 8000:8000 %IMAGE_NAME%:%IMAGE_TAG%'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*.json', allowEmptyArchive: true
        }
    }
}
