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
        stage("Params"){

            steps{
            checkout([$class: 'GitSCM', branches: [[name: 'Develop']], extensions: [], userRemoteConfigs: [[credentialsId: 'gitcred', url: 'https://github.com/richie312/email_recruiter_app_Flask.git']]])
            sh "echo $params.current_status"
            sh "echo $params.merged"
            sh "echo $params.branch"

             }
        }


        stage('BuildPreparations')
        {
//             when {
//                   expression { return params.branch == "Develop" && params.current_status == "closed" && params.merged == "closed" }
//               }
            steps
            {
                script
                {
                    // calculate GIT lastest commit short-hash
                    gitCommitHash = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
                    shortCommitHash = gitCommitHash.take(7)
                    // calculate a sample version tag
                    VERSION = shortCommitHash
                    // set the build display name
                    currentBuild.displayName = "#${BUILD_ID}-${VERSION}"
                    IMAGE = "$project_name:$ver"
                    println "${params.current_status}"
                }
            }
        }


        stage('PreBuild'){
        when {
                  expression { return params.branch == "Develop" && params.current_status == "closed" && params.merged == "closed" }
              }
            steps {
                    script {
                        sh "docker stop email_recruiter_app_Flask_web"
                        sh "docker stop email_recruiter_app_Flask_visualisation"
                        sh "docker rmi email_recruiter_app_Flask_web"
                        sh "docker rmi email_recruiter_app_Flask_visualisation"
                    }
                }
            }

        stage('BuildStage'){
        when {
                  expression { return params.branch == "Develop" && params.current_status == "closed" && params.merged == "closed" }
              }
            steps {
                    script {
                        sh "cd email_recruiter_app_Flask"
                        sh "docker-compose -f docker-compose.yml up --build"
                    }
                timeout(120){}
                script{
                    echo "The container is active and application is live @ localhost:5001"
                    }
                }
            }
        }
    }