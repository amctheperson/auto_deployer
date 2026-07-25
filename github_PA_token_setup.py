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
