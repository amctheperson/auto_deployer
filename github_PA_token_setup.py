import subprocess
import getpass


"""

			GitHub Personal Access Token Setup

	Page	Purpose

	1	PA Token Verification Function
	
	2-3	Main script

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

Main script

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










#					2


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
 

#					3


# <-- CTRL + B							    CTRL + F -->


# TODO

# check for existing token saved
# double checks for saving to file and attempting to change key

# stretch goal: check for expiration date, may require GitHub REST API usage
# actually it could only be the GitHub API via HTTP request
# https://stackoverflow.com/questions/69041150/github-personal-access-token-get-expiry

# Stretch goal 2: encrypt env file with dotenvx
# https://dotenvx.com/docs/secrets-in-python







































#					4


# <-- CTRL + B							    CTRL + F -->

