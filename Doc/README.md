# Project setup

## Google sheet

First of all, you need a Google account to set up the project.

Once connected to your account, you have to create a Google Sheet: https://docs.google.com/spreadsheets

Name it whatever you want.

## Google project & service account

The second step of the project setup will be the creation of a Google project and a service account.

To do this, go to: https://console.cloud.google.com

![Google console](img/console_google_menu.png)

Click on the project tab at the top left corner of the screen (next to the Google tab).

![Google console project](img/project_list.png)

Name it whatever you want.

![Google console project name](img/project_name.png)

Once the project is created, select this project.
Now, in the navigation menu, look for **APIs and services**

![Google API & services](img/api_and_services.png)

Click on ```Enable APIs and services```.
Look for ```Google Drive API``` and ```Google Sheets API```.

Once enabled, you have to create a service account to interact with your Google Sheet.
Go to ```Credentials```:

![Credentials](img/credentials.png)

Then click ```+ Create credentials``` and select ```Service account```:

![Service account creation](img/service_account.png)

Name it whatever you want once again.

For the second step of the service account creation, select the ```Editor``` role:

![Service accoutn role](img/editor_role.png)

(You can skip the third step)

## Auth key & configuration file...

Now that the service account is created, we need three more things:

- Create an auth key & download the configuration file
- Set the service account as an editor of the Google Sheet

First, go to your service account details and navigate to the ```Key``` section:

![Service account key](img/service_account_key.png)

Now, create a key and select ```json``` extension:

![Service account key](img/service_account_key_json.png)

Once the configuration file is downloaded, you need to place this file into the ```src``` directory of this project. It is recommended to rename this file.

To set the service account as an editor of the Google Sheet, you need to open your configuration file and look for the ```client_email```:

![Service account mail](img/client_email.png)

Now, go to your Google Sheet and share it with your service account, granting the account editor rights.

## .env file

The last step to configure this project is to create ```.env``` file at the root of the project directory.

![Env file example](img/env_file.png)

Create these two exact environment variables and fill them with the name of your configuration file and the name of your Google Sheet.

![Filled env file](img/filled_env.png)
