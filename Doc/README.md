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

- Create an auth key
- Download the configuration file
- Set the service account as an editor of the Google Sheet
