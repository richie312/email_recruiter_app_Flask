pipeline {
    agent any

    stages {
        stage('dev_build') {
            agent{
                dockerfile{
                    dir 'C:/Users/aritra_chatterjee/email_recruiter_app_Flask'
                    filename 'Dockerfile'
                    label 'docker'
                }
            }
            steps {
                script {
                
                    if (isUnix()){
                        sh "ls-la"
                    }
                    
                    else{
                        
                    bat "dir"
                }
            }
                script{
                    echo 'testing stage running'
                    sh "ls"
                }
            }
    }    
/*         stage('qa') {
    
            steps {
                script{
                git 'https://github.com/richie312/email_recruiter_app_Flask'
                }
            }
        }
        stage('activate_env'){
            steps {
                    script {
                        if (isUnix()){
                            sh "./email.sh"
                        }
                        
                        else{
                            
                        bat "./email.bat"
                    
                        }
                    }
                }
            } */
        stage('get_credentials'){
            steps {
                    withCredentials([usernameColonPassword(credentialsId: 'aritra_id_1', variable: 'aritra_credentials')]) {
                    // credentials
                    script{
                        echo "'${aritra_credentials}'!"

                    } 


                   }    
                }
            }
        }
    }