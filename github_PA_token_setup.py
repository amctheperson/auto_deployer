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
			
	5	Get Current Token Function

	5-8	Main script

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

Queries the active Github account token information via the GitHub CLI
about the current token's info relevant to the user (username and perms)

Input:
 	
	None

Output:
	Tuple of strings ->
		String including GitHub account username
		String including Github token perms	

"""

def getCurrentTokenInfo():

	info_query = subprocess.run(	"gh auth status " + 
					"--active " + 
					"--json hosts " + 
					"--jq " + "\'" +
						'.hosts' +
						'[\"github.com\"]' +
						'[0]' +
						'[\"login\"]'
							+ ','
						'.hosts' +
						'[\"github.com\"]' +
						'[0]' +
						'[\"scopes\"]'	
						+ "\'",
					shell=True,
					capture_output=True,
					text=True)

	if info_query.returncode != 0:
		raise RuntimeError(
			"Cannot get current authentication info \n" + 
			"when no GitHub account is currently logged in. \n")
		return None, None
	
	info_list = info_query.stdout.split('\n')
	info_list.pop()

	username_string = info_list[0] 
	token_perms_list = info_list[1].split(',') 
	token_perms_list = [item.strip() for item in token_perms_list]

	return (username_string, token_perms_list)
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

	# Query authentication statuses 
	# Filtering Github CLI JSON string output via jq expression

	query = subprocess.run(	"gh auth status " + 
						"--active " +
						"--json hosts " +
						"--show-token " + 
						"--jq " + 
							"\'.hosts" +
							"[\"github.com\"]" +
							"[0]" +
							"[\"token\"]\'",
						shell=True,
						capture_output=True,
						text=True)
	
	# Raise error if GitHub CLI was never authenticated
	# Detected by non-zero exit code when querying 

	if query.returncode != 0:

		logged_out_error_message = ("\t" +
			"No tokens have been used to authenticate a Github " +
			"account"+ 
			"\n\t\t" + 
			"on the CLI yet \n") 
			
		raise LookupError(logged_out_error_message)

		return None

	return query.stdout


#					4


# <-- CTRL + B						    	    CTRL + F -->


"""

Main script 

"""

# Checking for existing token (via local file) 
# and confirming token setup continuation



env_file_path = Path('./.env')

if env_file_path.exists():

	curUsername, curTokenPerms = getCurrentTokenInfo()

	print(	"\n" +
		"A token is already being used for Github " +
		f"account '{curUsername}'\n" + 
		"and with the following permissions: \n")

	for perm in curTokenPerms:
		print("\t" + f"- {perm}")
  	
	if confirmer("Confirm that this token should be overwritten") == 'n':
		print(	"\n" +
			"Existing token remains unchanged. \n")
		sys.exit(0)





















	
#					5


# <-- CTRL + B							    CTRL + F -->


"""

Main script (contd.)

"""

# Displaying instructions for generating a new Personal Access token

introduction_string = (
	"\n" +

	"In order to automate GitHub release deployment \n" +  
	"a valid GitHub PA (Personal Access) Token is required." +

	"\n\n" + 

	"GitHub PA Token generation can be accessed from this link:" +
 
	"\n\n\t" + 

		"https://github.com/settings/tokens/new" +
 
	"\n\n" +

	"The token should be generated with the following permissions:\n" + 

		"\t" + "-repo \t\t(1st category header) \n" +
 
		"\t" + "-read:org \t(subcategory under 4th category header " + 
		"'admin:org') \n" +

		"\t" + "-gists \t\t(small category header in middle of the page)" +
	"\n\n" +

	"Please verify that the GitHub account being used for PA Token " + 
	"generation has \n" + 
	"the ability to update releases in the repo " + 
	"intended for release deployment. \n")

print(introduction_string)










#					6


# <-- CTRL + B							    CTRL + F -->


"""

Main script (contd.)

"""

cur_token = getCurrentToken()

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
old_token = cur_token
new_token = supposed_token





















#					7


# <-- CTRL + B							    CTRL + F -->


"""

Main script (contd.)

"""

# Final confirmation of token change

print(	"\n" +
	"Provided token will authenticate Github " +
	f"account '{curUsername}'\n" + 
	"with the following permissions: \n")
print(curTokenPerms)
for perm in curTokenPerms:
	print("\t" + f"- {perm}")

if confirmer("Confirm that this token should be used") == 'n':
	
	# new_token was authenticated when verifying
	# so revert back to old_token if user declines confirmation
	
	subprocess.run(	"gh auth login " + 
				"--with-token " + 
				f" <<< '{old_token}'", 
			shell=True,
			capture_output=True)
		
	print(	"\n" +
		"Existing token remains unchanged. \n")
	sys.exit(0)

# Saving valid token to local .env file
# GitHub docs recommend this when using PA tokens in code

with open('.env', 'w') as file:
	file.write(f"GITHUB_CLI_KEY={new_token}")

authentication_complete_message = ("\n" +
	"Provided token was saved to local file and is now active. \n"
)

print(authentication_complete_message)









#					8


# <-- CTRL + B							    CTRL + F -->


# TODO


# Confirmer message migration to new script

# stretch goal: check for expiration date, may require GitHub REST API usage
# actually it could only be the GitHub API via HTTP request
# https://stackoverflow.com/questions/69041150/github-personal-access-token-get-expiry

# Stretch goal 2: encrypt env file with dotenvx
# https://dotenvx.com/docs/secrets-in-python







































#					9


# <-- CTRL + B							    

