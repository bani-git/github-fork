
A Python Flask web service to get Github Authorization and support forking a public repository
This project can be extended to support other Authorization servers such as Facebook, Twitter in the future.

**Getting started:**

app.py and service.app_factory.py contain the core functionality for this Python Flask App

**Deployment:**
The web service is deployed and hosted via Heroku and hosted at this location:
https://intense-basin-56365.herokuapp.com/

**Instructions to run in a web browser:**
1. Run https://intense-basin-56365.herokuapp.com/login to trigger Github Authorization.
This will prompt a Github login
2. Run https://intense-basin-56365.herokuapp.com/login/fork?repoowner=owner&reponame=name to create a fork.
Example : https://intense-basin-56365.herokuapp.com/login/fork?repoowner=octocat&reponame=Spoon-Knife

owner = Owner of the repository being forked

name = Name of the public repository being forked

A POST request handler in the webservice was used to handle creation of the fork.