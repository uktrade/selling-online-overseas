pipeline {

  agent {
    node {
      label 'docker.ci.uktrade.io'
    }
  }

  stages {

    stage('Prepare'){
      steps {
        script {
          echo "Cloning env var repo"
          dir ('paas_env') {
            git url: "${params.github_url}/${params.project_name}-envs.git", credentialsId: '16e11bb3-6c5a-4979-a512-4a9fb75feede'
          }

          sh "cp paas_env/${params.environment}/PaaSEnvFile vars.env"
          sh "echo 'CF_USERNAME=${params.cf_username}' >> vars.env"
          sh "echo 'CF_PASSWORD=${params.cf_password}' >> vars.env"
          sh "echo 'CF_APP_SPACE=${params.app_space}' >> vars.env"
          sh "echo 'CF_ORG=${params.paas_org}' >> vars.env"

          if ("${params.environment}" == "review") {
            sh "git branch --remotes --contains `git rev-parse HEAD` | grep -v HEAD > ${env.WORKSPACE}/.git_branch_name"
            branch = readFile "${env.WORKSPACE}/.git_branch_name"
            env.BRANCH_NAME = branch.replaceAll(/\s+origin\//, "").trim()
            sh "echo \"CF_APP_NAME=${params.app_name}-${env.BRANCH_NAME}\" >> vars.env"
          } else {
            sh "echo 'CF_APP_NAME=${params.app_name}' >> vars.env"
          }

          env.DEV_PORT = 'dummy'
          env.TEST_PORT = 'dummy'

          echo "Creating Docker container"
          sh "docker-compose pull build"
        }
      }
    }

    stage ('Build') {
      steps {
        script {
          echo "Building application"
          sh "docker-compose build build"
        }
      }
    }

    stage('Deploy'){
      steps {
        echo "Uploading to PaaS"
        script {
          echo "Deploying to GDS"
          sh "docker-compose run build /project/deploy.sh"
        }
      }
    }

  }
}
