from pathlib import Path
import subprocess

from gh_token_setup import isValidToken


def gh_token_setup_check():

	# Check if .env file exists first
	
	env_file_path = Path('./.env')
	
	if not env_file_path.exists():

		return "FAIL_NO_TOKEN_SAVED"


	# Load saved token into string

	loading_token_process = subprocess.run(	
						"source '.env'; " +
						"echo $GITHUB_CLI_KEY",
					shell=True,
					capture_output=True,
					text=True)

	loaded_token = loading_token_process.stdout.strip()


	# Check if loaded token is still valid	

	if not isValidToken(loaded_token): 
		
		return "FAIL_SAVED_TOKEN_INVALID" 
	

	return "PASS"
	
	
# TODO
	
	# check for signature file

	# check if repo provided is deployable

	

