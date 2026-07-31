import subprocess


"""	
Function: Validating GitHub Personal Access token 
	
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
	"intended for release deployment. \n"	
	)

print(introduction_string)


supposed_token_input_message = (
	"\n" + 
	"Please enter a GitHub Personal Access Token " + 
	"meeting the above requirements:" + 
	"\n\n\t"
	)

supposed_token = input(supposed_token_input_message) 

while (not isValidToken(supposed_token)):
	print(
		"\n" +
		f"'{supposed_token}' was not able to authenticate. " +
		"Please try again. \n"
	)

	supposed_token = input(supposed_token_input_message) 

# for testing just pipe env var aka "github auth login <<< ($TOKEN)"
 
# TODO
# migrate to getpass for input for sensitivity
	# https://docs.python.org/3/library/getpass.html
# save validated_token to text file
