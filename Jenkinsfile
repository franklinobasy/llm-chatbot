pipeline {
    agent any

    environment {
        ANSIBLE_PLAYBOOK_PATH = '/path/to/ansible/playbook/deploy.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    checkout scm
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    // Run Ansible playbook
                    sh "ansible-playbook -i '${ANSIBLE_PLAYBOOK_PATH}'"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! You can add more post-build steps here.'
        }
        failure {
            echo 'Pipeline failed! You can add more post-build steps here.'
        }
    }
}
