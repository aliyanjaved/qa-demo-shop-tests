pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build images') {
            steps { sh 'docker compose build' }
        }
        stage('Run tests') {
            steps {
                sh 'mkdir -p reports'
                sh 'docker compose --profile test run --rm tests'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            sh 'docker compose down -v || true'
        }
    }
}
