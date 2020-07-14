pipeline {
    agent any
    environment {
            docker_user = 'richie31'
            registryCredential = 'dockerhub'
            project_name = "jban"
            semi_colon = ':'
            slash = '/'
            ver = "ver"
    }

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
                        bat"""  echo Intializing docker authentication
                                docker login -u ${docker_user} -p Kevalasya@123"
                                set image_name=${docker_user}${slash}${project_name}${semi_colon}${ver}${BUILD_NUMBER}
                                docker build --no-cache -t %image_name% .
                                docker run -d %image_name%
                                echo Waiting for docker recently created container to initialize.
                        """
                    }
                timeout(10){}
                script{
                    echo "The container is active and application is live @ localhost:5001"
                    }
                }
            }
        stage('post_build'){
            steps {
                    script {
                        bat """
                        echo Updating the docker hub with the recently created image.
                        set image_name=${docker_user}${slash}${project_name}${semi_colon}${ver}${BUILD_NUMBER}
                        bat docker push %image_name%
                        echo Image has been successfully uploaded to the docker hub."""

                    }
                }
            }
        }
    }