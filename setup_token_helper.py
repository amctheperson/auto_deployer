import subprocess
import json



"""

			GitHub Personal Access Token Setup

	Page	Purpose

	1	PA Token Verification Function

	2	Get Info on Current Token's GitHub Authentication Function 
	
	3	Get Current Token Function


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


#					3


# <-- CTRL + B							    

