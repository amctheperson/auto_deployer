import subprocess

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

login_process_code = 97
validated_token = None
while login_process_code != 0:

	supposed_token = \
	(
		input(
			"\n" + 
			"Please enter a GitHub Personal Access Token " + 
			"meeting the above requirements:" + 
			"\n\n\t"
		)

	)

	# Using subprocess class to run shell commands

		# shell flag required for single command

		# capture_output flag prevents std out and std err
		# from printing to console and instead can be accessed
		# as a public class property of CompletedProcess obj 
		# made from run()

	subprocess.run(	"gh auth logout",
			shell=True,
			capture_output=True)

	# return code class property of CompletedProcess
	# can be used to check if token authenticates successfully (0 if so) 
			
	login_attempt = subprocess.run(	"gh auth login " + 
						"--with-token " + 
						f" <<< '{supposed_token}'", 
					shell=True,
					capture_output=True)

	login_process_code = login_attempt.returncode

	if login_process_code == 0:
		validated_token = supposed_token
		break

	print(	"\n" +
		f"'{supposed_token}' is not a valid GitHub PA token. \n")			

#print(login_attempt.returncode)

# for testing just pipe env var aka "github auth login <<< ($TOKEN)"
 
# TODO
# migrate to getpass for input for sensitivity
	# https://docs.python.org/3/library/getpass.html
# turn loop into functions to make loop more readable
# save validated_token to text file
