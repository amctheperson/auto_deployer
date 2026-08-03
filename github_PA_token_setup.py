import subprocess
import getpass
import sys
import json

from pathlib import Path

"""

			GitHub Personal Access Token Setup

	Page	Purpose

	1	PA Token Verification Function

	2	Get Info on Current Token's GitHub Authentication Function 

	3	Confirmer function
			
	4-5	Get Current Token Function

	6-7	Main script

"""





























#					0


#							            CTRL + F -->


"""	
Personal Access Token Verification Function
	
Input:
 
	(String) supposed_token | token to be validated

Output:

	(boolean) 
	True = token is valid and can be used to log in to GitHub CLI
	False = token is invalid
"""

def isValidToken(supposed_token):

	# Note: Github CLI reauthenticates token even if logged in already
	# Therefore 'gh auth logout' is unnecessary

	# Use subprocess package to attempt token authentication 
	
	login_attempt = subprocess.run(	"gh auth login " + 
						"--with-token " + 
						f" <<< '{supposed_token}'", 
					shell=True,
					capture_output=True)

	# Get exit code of token authentication attempt subprocess

	login_process_code = login_attempt.returncode

	if login_process_code == 0: return True

	return False

















#					1


# <-- CTRL + B							    CTRL + F -->


"""
Get Info on Current Token's GitHub Authentication Function 

Parses command-line output of 'gh auth status' to get relevant info to user
(Current authenticated Github account username, current token perms) 

Note:
 	
	Function will raise RuntimeError if no GitHub account is currently
	logged in

Input:
 	
	None

Output:
	Tuple of strings ->
		String including GitHub account username
		String including Github token perms	

"""

def getCurrentAuthenticationInfo():

	auth_status_process = subprocess.run(	'gh auth status -a',
						shell=True,
						capture_output=True,
						text=True)
	if auth_status_process.returncode != 0:
		raise RuntimeError(
			"Cannot get current authentication info \n" + 
			"when no GitHub account is currently logged in. \n")
		return None
	
	auth_status_stringList = auth_status_process.stdout.split('\n')
	auth_status_stringList.pop()
	
	account_info_string = auth_status_stringList[1]
	token_perms_string = auth_status_stringList[5]
	
	return (account_info_string, token_perms_string)










#					2


# <-- CTRL + B							    CTRL + F -->


"""
Confirmer function

For general use, requires user to input a 'y' or 'n'

Note to self: 
	Migrate this function to new Python script class 
	so it can be used for future scripts 
	and refactor signature_setup script with this

Input:

	(String)  prompt | Message to user explaining confirmation

Output:

	(String) response | User's confirmation -> either 'y' or 'n'
 
"""

def confirmer(prompt):
	
	response = input(	"\n" + 
				prompt + " (y/n): " + 
				"\n\n\t")
	
	while(response != 'y' and response != 'n'):
		print(	"\n" + 
			f"'{response}' is not a valid response. \n")
		
		response = input(	"\n" + 
					prompt + " (y/n): " + 
					"\n\n\t")
	return response	

 















#					3


# <-- CTRL + B							    CTRL + F -->


"""
Get Current Token Function

Uses Github CLI tool to query about all authentications 
and parses the JSON output to find the active account's token

Input:

	None

Output:
	(String) | Current token (used for the active GitHub account)

"""

def getCurrentToken():

	# Query authentication statuses and receive JSON string as a response

	auth_status_process = subprocess.run(	"gh auth status -a " +
							"--json hosts " +
							"--show-token",
						shell=True,
						capture_output=True,
						text=True)

	# Raise error if GitHub CLI was never authenticated
	# Detected by non-zero exit code when querying authentication status

	if auth_status_process.returncode != 0:

		logged_out_error_message = ("\t" +
			"No tokens have been used to authenticate a Github " +
			"account"+ 
			"\n\t\t" + 
			"on the CLI yet \n") 
			
		raise LookupError(logged_out_error_message)

		return None

	# Load JSON string into Json object  
	
	authentication_json = json.loads(auth_status_process.stdout)


	# Parse JSON for token of active Github account

	active_account = authentication_json["hosts"]["github.com"][0]
	return active_account["token"]

#					4


# <-- CTRL + B						    	    CTRL + F -->


"""

Main script 

"""

# Checking for existing token (via local file) 
# and confirming token setup continuation



env_file_path = Path('./.env')

if env_file_path.exists():

	curAccountInfo, curTokenPerms = getCurrentAuthenticationInfo()

	# Note that f-strings are not used for printing here because
	# these variables are already strings

	print(	"\n" +
		"A token is already being used in the following manner: \n" +
		curAccountInfo + "\n" +
		curTokenPerms + "\n")
	
	if confirmer("Confirm that this token can be overwritten") == 'n':
		print(	"\n" +
			"Existing token remains unchanged. \n")
		sys.exit(0)





















	
#					5


# <-- CTRL + B							    CTRL + F -->


"""

Main script (contd.)

"""

# Asking user to input PA token, ensuring validity

supposed_token_input_message = (
	"\n" + 
	"Please enter a GitHub Personal Access Token " + 
	"meeting the above requirements:" + 
	"\n\n\t"
	)

supposed_token = getpass.getpass(prompt=supposed_token_input_message,
				 echo_char='*') 

while (not isValidToken(supposed_token)):
	print(
		"\n" +
		"Provided token could not be verified, " + 
		"please double-check your input. \n"
	)
	supposed_token = getpass.getpass(prompt=supposed_token_input_message,
					 echo_char='*') 

valid_token = supposed_token

# Saving valid token to local .env file
# GitHub docs recommend this when using PA tokens in code

with open('.env', 'w') as file:
	file.write(f"GITHUB_CLI_KEY={valid_token}")

authentication_complete_message = ("\n" +
	"Token verified and saved to local file. \n"
)

# Note to self:

# loading token into bash script is simple as

# source .env
# github auth login <<< $GITHUB_CLI_KEY

print(authentication_complete_message)

# for testing just pipe env var aka "github auth login <<< ($TOKEN)"
 

#					6


# <-- CTRL + B							    CTRL + F -->


# TODO

# Refactor get authentication info with JSON parsing functionality

# Final double check for saving to file and attempting to change key


# Confirmer message migration to new script

# stretch goal: check for expiration date, may require GitHub REST API usage
# actually it could only be the GitHub API via HTTP request
# https://stackoverflow.com/questions/69041150/github-personal-access-token-get-expiry

# Stretch goal 2: encrypt env file with dotenvx
# https://dotenvx.com/docs/secrets-in-python



































#					7


# <-- CTRL + B							    

