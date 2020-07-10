pipeline {
    agent any

    stages {
        stage('dev') {
            steps {
                script {
                
                    if (isUnix()){
                        sh "ls-la"
                    }
                    
                    else{
                        
                    bat "dir"
                
                }
            
            }    
        }
            
    }
    
    stage('qa') {
        steps {
            git 'https://github.com/richie312/email_recruiter_app_Flask'
        }
    stage('activate_env'){
         step{
                    if (isUnix()){
                        sh "./email.sh"
                    }
                    
                    else{
                        
                    bat "./email.bat"
                
                }
           }

         
     
         }   
        }
    }
}