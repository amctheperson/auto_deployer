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

supposed_token = \
(
	input(
		"\n" + 
		"Please enter a GitHub Personal Access Token meeting " + 
		"the above requirements:" + 
		"\n\n\t"
	)

)

#subprocess.run("testVar='hello Shell'", shell=True)

# Using subprocess class to run shell commands inside Python script
# making std output of process when completed accessible
# and turning the byte sequence into a string automatically

# this is good info but there is a discrete easily acessible property
# for checking if a process ran without errors

# return code
		# returns 0 when process has no issues
		# returns 1 when process has stderror

# documentation says exit code 0 typically means it ran successfully

# we are still capturing output so that error isn't printed to std err console

subprocess.run(	"gh auth logout",
		shell=True,
		capture_output=True)
		
testCompletedProcess = subprocess.run(	"gh auth login " + 
					"--with-token " + 
						f" <<< '{supposed_token}'", 
					shell=True,
					capture_output=True)

# removing trailing white space

#testString = testCompletedProcess.stderr.rstrip()

print(testCompletedProcess.returncode)
#print(testString)
#print(len(testString))


# TODO call bash and gh auth login PA token via txt file
# for testing just pipe env var aka "github auth login <<< ($TOKEN)" 	
