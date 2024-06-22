# API Token Generator for Stack Overflow Enterprise
A Python script that streamlines the process of creating an API token for Stack Overflow Enterprise (SOE). 

The full, manual process for creating an API token can be found here in the KB article titled [Secure API Token Generation Using OAuth with PKCE](https://support.stackenterprise.co/support/solutions/articles/22000286119-secure-api-token-generation-using-oauth-with-pkce).

If you're using the Basic or Business version of Stack Overflow for Teams, this project is not for you. Creating a personal access token is already fairly quick and easy for you ([KB article](https://stackoverflow.help/en/articles/4385859-stack-overflow-for-teams-api)).

## Table of Contents
* [Requirements](https://github.com/jklick-so/soe_token_generator?tab=readme-ov-file#requirements)
* [Setup](https://github.com/jklick-so/soe_token_generator?tab=readme-ov-file#setup)
* [Usage](https://github.com/jklick-so/soe_token_generator?tab=readme-ov-file#usage)
* [How it Works](https://github.com/jklick-so/soe_token_generator?tab=readme-ov-file#how-it-works)
* [Support, security, and legal](https://github.com/jklick-so/soe_token_generator?tab=readme-ov-file#support-security-and-legal)


## Requirements
* Stack Overflow Enterprise (no support Stack Overflow Business or Basic)
* Python 3.8 or higher ([download](https://www.python.org/downloads/))
* Operating system: Linux, MacOS, or Windows

## Setup

[Download](https://github.com/jklick-so/soe_token_generator/archive/refs/heads/main.zip) and unpack the contents of this repository

**Installing Dependencies**

* Open a terminal window (or, for Windows, a command prompt)
* Navigate to the directory where you unpacked the files
* Install the dependencies:
```sh
python3 -m pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
```

> NOTE: Depending on your installation of Python, you may need to use `python` or `py` instead of `python3` in the command above. If `python3` is not a recognized command, you can check which command to use by running `python --version` or `py --version` in your terminal and seeing which responds with the installed Python version.


**Obtain a Client ID**
* Go to the Stack Overflow Enterprise web interface
* Go to your user profile (top-right corner of the interface)
* Go to the "Settings" tab (next to the "Profile" and "Activity" tabs)
* Select "API Applications"
* If you don't already have an "Active API Application" listed, you'll need to create a new one by using the "Create an API Application" form. 
    * Fill in an "API application name" of your choosing. It can be anything you want, but it helps to provide a name that helps you remember its purpose.
    * For "Domain" you can use the same URL as your SOE instance (e.g. YOUR-SUBDOMAIN.stackenterprise.co)
    * Then use the "Create API Application" button
* If you have an API application, take note of the "Client Id" number, which can be found just under the bolded API application name.

> IMPORTANT NOTE: If you're going to want your API token to have write access -- i.e. you'll be using the token to edit or post new content to SOE, rather than simply gathering data from SOE --, you'll want to use the dropdown box in the "Status" column of the API application and change it from "Read-only" to "Read-write"


## Usage

In a terminal window, navigate to the directory where you unpacked the script. Run the script with the following format:

```sh
python3 token_generator.py
```

* At the beginning of the script, you'll be prompted for the following information:
    * The URL of your Stack Overflow Enterprise instance (e.g. YOUR-SUBDOMAIN.stackenterprise.co)
    * The client ID you obtained in the [Setup](https://github.com/jklick-so/soe_token_generator?tab=readme-ov-file#setup) section of these instructions
    * Whether or not you want your token to have write permissions (see note at the bottom of the Client ID instructions above)
    * Whether or not you want your token to have an expiration. By default, all API tokens expire in 24 hours.
* The script will then open a browser tab where you will need to authenticate with Stack Overflow Enterprise.
* After authenticating, you'll be redirected to a new URL. Copy the entire URL from your browser tab and paste it into the window where you're running the script.
* Lastly, the script will output your API token.

## How it Works

For those of you who are familiar with the authorization code flow with PKCE, here is what the script is performing behind the scenes in order to simplify your life:
* Generates a Base64-encoded code verifier
* Generates a code challenge by hashing the code verifier with SHA256, then encoding it with Base64
* Generates a randomized 10-character string to act as the "state" parameter
* Combines all the necessary parameters to create the complex URL for generating an authorization code, which is laborious when done manually
* Parses the resulting URL to extract the authorization code
* Creates and sends the POST request to obtain the final the API token
* Parses the final HTTP response to extract the token string

## Support, security, and legal
Disclaimer: this project is a labor of love that comes with no formal support from Stack Overflow. 

If you run into issues using the script, please [open an issue](https://github.com/jklick-so/soe_token_generator/issues). You are also welcome to edit the script to suit your needs, steal the code, or do whatever you want with it. It is provided as-is, with no warranty or guarantee of any kind. If the creator wasn't so lazy, there would likely be an MIT license file included.
