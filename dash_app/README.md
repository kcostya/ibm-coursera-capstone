## Getting Started with Python on IBM Cloud

Sample Python Dash app (Flask inside) with instruction on setting up a development environment and deploying to IBM Cloud.

## Prerequisites

You'll need the following:
* [IBM Cloud account](https://console.ng.bluemix.net/registration/)
* [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads)
* [Git](https://git-scm.com/downloads)
* [Python](https://www.python.org/downloads/)
* [Docker and a Docker Hub account](https://hub.docker.com/)

1. Cloud Foundry apps require a manifest file with some application configurations to be defined. These must be in the application root (dash-app directory in this case). The `manifest.yml` file must be created and should contain the following:
```
applications:
- name: <YOUR APP NAME>
  random-route: true
  memory: 256M
  docker:
     image: <YOUR DOCKERHUB USERNAME>/python-dash
```
2. The application dependencies must be defined in the `requirements.txt` file. Create this file in the app directory:
```
!pip freeze > requirements.txt
```
3. Next, the Docker file application must be defined. In the app directory, create a Dockerfile file and add the following to it:
```
FROM python:3.6.4-slim
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . /.
CMD ["python", "app.py"]
```
4. From the deploy directory, build the Docker image with the following command:
```
docker image build -t <YOUR DOCKERHUB USERNAME>/python-dash .
```
Take note of the . at the end of the command, which specifies that you are building the image based on the Dockerfile in this directory.
5. Before you can deploy the application, it needs to be pushed to a container registry. In this case, Docker Hub will be used. Log into Docker Hub with the following command, and enter your username and password:
```
docker login
```
Push the image to Docker Hub with the following command:
```
docker push <YOUR DOCKERHUB USERNAME>/python-dash
```
Upon completing the above, your app directory should be as follows:
```
- dash-app
    - app.py
    - Dockerfile
    - manifest.yml
    - requirements.txt
    - pipeline.pickle
    - Procfile
    - setup.py
    - utils.py
```  
6. Deploy the application from the CLI
Deploy the application to Cloud Foundry on IBM Cloud. This will be done with the IBM Cloud CLI. Regardless of whether you’re using the Cloud Foundry Python runtime or the Cloud Foundry Docker runtime, the following steps should be the same.

Navigate to your app directory from your command line.

Download the IBM Cloud CLI if you do not already have it as directed here or as shown below:

For Linux/Mac, you can download it with the following command:
```
curl -sL https://raw.githubusercontent.com/IBM-Cloud/developer-tools-installer/master/linux-installer/idt-installer | bash
```
And for Windows from Powershell as an administrator with:
```
Set-ExecutionPolicy Unrestricted; iex(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/IBM-Cloud/developer-tools-installer/master/windows-installer/idt-win-installer.ps1')
```
Verify your installation by running the following command:
```
ibmcloud --help
```
After you have verified that the CLI is correctly installed, log into IBM Cloud, and target Cloud Foundry from the CLI with the following:
```
ibmcloud login
ibmcloud target --cf
```
Note that if you are using a federated ID and see the following when running ibmcloud login:
```
You are using a federated user ID, please use one time passcode ( C:\Program Files\IBM\Cloud\bin\ibmcloud.exe login --sso ), or use API key ( C:\Program Files\IBM\Cloud\bin\ibmcloud.exe --apikey key or @key_file ) to authenticate.
```
First try to log in using `ibmcloud login --sso`, and if that does not work, use the API key method.

Push your application to Cloud Foundry from the CLI:
```
ibmcloud cf push
```
When the deployment has completed, you will see something like the following output:
```
 name:              docker-capstone
 requested state:   started
 instances:         1/1
 usage:             256M x 1 instances
 routes:            https://<HOSTNAME>.<REGION>.mybluemix.net
 last uploaded:     Mon 14 Jan 14:26:10 SAST 2019
 stack:             cflinuxfs2
 buildpack:         python_buildpack
 start command:     python app.py
```
View your app at the URL listed in the output of the push command, for example, myUrl.mybluemix.net.
