pipeline {
    agent any

    stages {
        stage('build_preparation') {
                steps {
                    script{
                        git 'https://github.com/richie312/email_recruiter_app_Flask'
                    }
                }
    }    
        stage('build_stage'){
            steps {
                    script {
                        bat "docker build --no-cache -t jban:ver0.1 ."
                    }
                }
            }
        }
    }