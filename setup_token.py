import subprocess
import getpass
import sys

from setup_token_helper import *
from setup_helper import *


from pathlib import Path

"""

		Main Script for (GitHub Personal Access) Token Setup


	Page	Purpose

	1	Check for Existing Saved Token + Confirm Token Overwrite
 
	2	Printing Instructions on Generating New Github PA Token		

	3	User Inputs New Valid Token
			
	4	Finalizing Token Save via New Token Info and User Confirmation 


"""


























#					0


#							            CTRL + F -->


"""

				   Main script 

"""


# Checking for existing local token file 

env_file_path = Path('./.env')

if env_file_path.exists():

	# Confirming overwrite of existing token 

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





















	
#					1


# <-- CTRL + B							    CTRL + F -->


"""

				   Main script 
				    (contd.)
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

				   Main script 
				    (contd.)
"""


# Asking user to input new token

supposed_token_input_message = (
	"\n" + 
	"Please enter a GitHub Personal Access Token " + 
	"meeting the above requirements:" + 
	"\n\n\t"
	)

supposed_token = getpass.getpass(prompt=supposed_token_input_message,
				 echo_char='*') 


# Sanitize input by checking if provided input is a valid token

while (not isValidToken(supposed_token)):
	print(
		"\n" +
		"Provided token could not be verified, " + 
		"please double-check your input. \n"
	)
	supposed_token = getpass.getpass(prompt=supposed_token_input_message,
					 echo_char='*') 



old_token = getCurrentToken()
new_token = supposed_token
















#					3


# <-- CTRL + B							    CTRL + F -->


"""

				   Main script 
				    (contd.)
"""


# Provide relevant info to user on new token

print(	"\n" +
	"Provided token will authenticate Github " +
	f"account '{curUsername}'\n" + 
	"with the following permissions: \n")

for perm in curTokenPerms:
	print("\t" + f"- {perm}")


# Final confirmation of token change

if confirmer("Confirm that this token should be used") == 'n':
	
	# Revert back to old_token on gh authentication if token change aborted
	# as new_token was authenticated when verifying via isValidToken
	
	subprocess.run(	"gh auth login " + 
				"--with-token " + 
				f" <<< '{old_token}'", 
			shell=True,
			capture_output=True)
		
	print(	"\n" +
		"Existing token remains unchanged. \n")

	sys.exit(0)

# Saving new token locally as .env file
# (as recommended by GitHub docs) 

with open('.env', 'w') as file:
	file.write(f"GITHUB_CLI_KEY={new_token}")

authentication_complete_message = ("\n" +
	"Provided token was saved to local file and is now active. \n"
)

print(authentication_complete_message)




#					4


# <-- CTRL + B							    CTRL + F -->


# TODO


# Confirmer message migration to new script

# stretch goal: check for expiration date, may require GitHub REST API usage
# actually it could only be the GitHub API via HTTP request
# https://stackoverflow.com/questions/69041150/github-personal-access-token-get-expiry

# Stretch goal 2: encrypt env file with dotenvx
# https://dotenvx.com/docs/secrets-in-python







































#					5


# <-- CTRL + B							    

