# PredicteurClauses on IBM Cloud

This application is made with Python 3, Cloudant DB and Flask. This application expose GUI and web service.
To get started, we'll take you through a this Python Flask app, help you set up a development environment, deploy to IBM Cloud and add a Cloudant database.

The following instructions are for deploying the application as a Cloud Foundry application. To deploy as a container to **IBM Cloud Kubernetes Service** instead, [see README-kubernetes.md](kubernetes/README-kubernetes.md)

## Prerequisites

You'll need the following:
* [IBM Cloud account](https://console.ng.bluemix.net/registration/)
* [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads)
* [Git](https://git-scm.com/downloads)
* [Python](https://www.python.org/downloads/)

## 1. Clone the sample app

Now you're ready to start working with the app. Clone the repo and change to the directory where the sample app is located.
  ```
git clone https://github.com/IBM-Cloud/get-started-python
cd get-started-python
  ```

  Peruse the files in the *get-started-python* directory to familiarize yourself with the contents.

## 2. Run the app locally

Install the dependencies listed in the [requirements.txt](https://pip.readthedocs.io/en/stable/user_guide/#requirements-files) file to be able to run the app locally.

You can optionally use a [virtual environment](https://packaging.python.org/installing/#creating-and-using-virtual-environments) to avoid having these dependencies clash with those of other Python projects or your operating system.
  ```
pip install -r requirements.txt
  ```

Run the app.
  ```
python hello.py
  ```

 View your app at: http://localhost:8000

## 3. Prepare the app for deployment

To deploy to IBM Cloud, it can be helpful to set up a manifest.yml file. One is provided for you with the sample. Take a moment to look at it.

The manifest.yml includes basic information about your app, such as the name, how much memory to allocate for each instance and the route. In this manifest.yml **random-route: true** generates a random route for your app to prevent your route from colliding with others.  You can replace **random-route: true** with **host: myChosenHostName**, supplying a host name of your choice. [Learn more...](https://console.bluemix.net/docs/manageapps/depapps.html#appmanifest)
 ```
 applications:
 - name: PredicteurClauses
   random-route: true
   buildpack: https://github.com/cloudfoundry/buildpack-python.git
   memory: 512M
 ```


## 4. Deploy the app

You can use the Cloud Foundry CLI to deploy apps.

Choose your API endpoint
   ```
cf api <API-endpoint>
   ```

Replace the *API-endpoint* in the command with an API endpoint from the following list.

|URL                             |Region          |
|:-------------------------------|:---------------|
| https://api.ng.bluemix.net     | US South       |
| https://api.eu-de.bluemix.net  | Germany        |
| https://api.eu-gb.bluemix.net  | United Kingdom |
| https://api.au-syd.bluemix.net | Sydney         |

Login to your IBM Cloud account

  ```
cf login
  ```

From within the *get-started-python* directory push your app to IBM Cloud
  ```
cf push
  ```

This can take a minute. If there is an error in the deployment process you can use the command `cf logs <Your-App-Name> --recent` to troubleshoot.

When deployment completes you should see a message indicating that your app is running.  View your app at the URL listed in the output of the push command.  You can also issue the
  ```
cf apps
  ```
  command to view your apps status and see the URL.

## 5. Add a database

Next, we'll add a NoSQL database to this application and set up the application so that it can run locally and on IBM Cloud.

1. Log in to IBM Cloud in your Browser. Browse to the `Dashboard`. Select your application by clicking on its name in the `Name` column.
2. Click on `Connections` then `Connect new`.
2. In the `Data & Analytics` section, select `Cloudant NoSQL DB` and `Create` the service.
3. Select `Restage` when prompted. IBM Cloud will restart your application and provide the database credentials to your application using the `VCAP_SERVICES` environment variable. This environment variable is only available to the application when it is running on IBM Cloud.

Environment variables enable you to separate deployment settings from your source code. For example, instead of hardcoding a database password, you can store this in an environment variable which you reference in your source code. [Learn more...](/docs/manageapps/depapps.html#app_env)

## 6. Use the database

We're now going to update your local code to point to this database. We'll create a json file that will store the credentials for the services the application will use. This file will get used ONLY when the application is running locally. When running in IBM Cloud, the credentials will be read from the VCAP_SERVICES environment variable.

1. Create a file called `vcap-local.json` in the `get-started-python` directory with the following content:
  ```
  {
    "services": {
      "cloudantNoSQLDB": [
        {
          "credentials": {
            "username":"CLOUDANT_DATABASE_USERNAME",
            "password":"CLOUDANT_DATABASE_PASSWORD",
            "host":"CLOUDANT_DATABASE_HOST"
          },
          "label": "cloudantNoSQLDB"
        }
      ]
    }
  }
  ```

2. Back in the IBM Cloud UI, select your App -> Connections -> Cloudant -> View Credentials

3. Copy and paste the `username`, `password`, and `host` from the credentials to the same fields of the `vcap-local.json` file replacing **CLOUDANT_DATABASE_USERNAME**, **CLOUDANT_DATABASE_PASSWORD**, and **CLOUDANT_DATABASE_URL**.

3. Select your runtime

Create a file runtime.txt where manifest.yml resides, add the desired python version

  ```
python-3.7.2
  ```

4. Run your application locally.
  ```
python hello.py
  ```

  View your app at: http://localhost:8000. Any names you enter into the app will now get added to the database.

5. Make any changes you want and re-deploy to IBM Cloud!
  ```
  cf push
  ibmcloud cf push PredicteurClauses -b https://github.com/cloudfoundry/python-buildpack.git#v1.6.34
  ibmcloud cf logs PredicteurClauses --recent
    ```

  check version of package
    ```
  pip3 show nltk
    ```

  View your app at the URL listed in the output of the push command, for example, *myUrl.mybluemix.net*.

6. Liens utiles
  ```
https://github.com/POC-Mediation/www-py-ml
https://valeriadiportela.sytes.net/DEMO/www-py-ml.git
  ```

7. Publication GIT

Create a new repository on the command line
  ```
  touch README.md
  git init
  git add README.md
  git commit -m "first commit"
  git remote add origin https://valeriadiportela.sytes.net/DEMO/www-py-ml.git
  git push -u origin master
  ```
Push an existing repository from the command line
  ```
  git remote add origin https://valeriadiportela.sytes.net/DEMO/www-py-ml.git
  git push -u origin master
  ```
How to insert existing repo into gogs or git

Just update the remote address.
first,remove your remote origin
```
git remote rm origin
```

second,add new remote origin address
```
git remote add origin git@your_gogs_repos_here.com
```

at last,push your master branch code
```
git push origin master
```



8. Executer localement l'application

Install the dependencies listed in the requirements.txt External link icon file to be able to run the app locally.

You can optionally use a [virtual environment](https://packaging.python.org/tutorials/installing-packages/#creating-and-using-virtual-environments) icon to avoid having these dependencies clash with those of other Python projects or your operating system.

  ``` bash
pip3 -m pip install -r requirements.txt
  ```

Executer l'application
  ``` bash
python3 hello.py
  ```  

8. Déployer l'application

Login to IBM Cloud
  ```
  ibmcloud login
  ```

If you have a federated user ID, instead use the following command to log in with your single sign-on ID. See [Logging in with a federated ID](https://cloud.ibm.com/docs/cli/login_federated_id.html?locale=en-US) to learn more.
  ```
  ibmcloud login --sso
  ```

Target Cloud Foundry org and space
  ```
  ibmcloud target --cf
  ```

From within the get-started-python directory push your app to IBM Cloud
  ```
  ibmcloud cf push
  ```

This can take a minute. If there is an error in the deployment process you can use the command ibmcloud cf logs <Your-App-Name> --recent to troubleshoot.
