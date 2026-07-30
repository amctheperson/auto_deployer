"""

Purpose: Script for setting up signature file if necessary

"""

from pathlib import Path



# Checking for existing signature file, parsing and displaying it
# and confirming if user wants to continue with signature setup

sig_file_path = Path('./signature_details.txt')
if sig_file_path.exists():
	with open('signature_details.txt', 'r') as sig_file:
		old_builder_key = sig_file.readline().rstrip()
		sig_file.readline() # key is used twice
		old_builder_name = sig_file.readline().rstrip()
		old_builder_department = sig_file.readline().rstrip()
		old_builder_company = sig_file.readline().rstrip()
		old_builder_city = sig_file.readline().rstrip()
		old_builder_region = sig_file.readline().rstrip()
		old_builder_country = sig_file.readline().rstrip()
		
		old_builder_signature_display = (
			"\n" + 
			f"{old_builder_name} | {old_builder_company} " + 
			f"- {old_builder_department} \n" +
			f"{old_builder_city}, {old_builder_region}, " + 
			f"{old_builder_country} \n" +
			f"(Auth key = {old_builder_key}) \n"	
		)

		print(
			"\n" +
			"A signature has already been saved locally, " +
			"it appears as follows:\n" +
			f"{old_builder_signature_display}"
		) 
	
		overwrite_confirm_message = (
			"\n" + 
			"Please confirm that this signature can be " + 
			"overwritten by new input. (y/n):"
			"\n\n\t")

		overwrite_confirm = input(overwrite_confirm_message)

		while not (	overwrite_confirm == 'y' or 
				overwrite_confirm == 'n'):

			print(
				"\n" + 
				f"'{overwrite_confirm}' is not " + 
				"a valid input. \n")

			overwrite_confirm = input(overwrite_confirm_message)
			
		if overwrite_confirm == 'n':
			print(
				"\n" + 
				"Confirmation rejected, signature remains " +
				"unmodified.\n" 
			)
			exit()
		
# Main script	

introduction_string = (	
	"\n" + 
	"In order for an Android application .apk file to be fully " + 
	"installable \n" +
	"it needs to be signed with the information of the person \n" +
	"who built the application (presumably for liability reasons)." + 
	"\n\n" +
	"The following prompts will ask and save this info in a local " + 
	"text file \n" +
	"for future build automation.\n"
)

print(introduction_string)

# Getting user employment info

builder_name = 	(
	input(	
		"Please enter the full name of the person initializing \n" +
		"build automation (e.g. 'John Smith'):" + 
		"\n\n\t")
	)

builder_company = (
	input(
		"\n" +
		f"Please enter the name of the company that {builder_name}\n" + 
		"is automating builds for (e.g. 'Google'):" +
		"\n\n\t")
	)
		
builder_department = (
	input(
		"\n" + 
		f"Please enter the department name that {builder_name} \n" +
		f"is under at {builder_company} ('N/A' is acceptable also):" +
	 	"\n\n\t")
	)

# Getting user residential info

builder_city = (
	input(
		"\n" + 
		"Please enter the city name associated with \n"
		f"the current location of {builder_name} " +
		"(e.g. 'Seattle'):" 
		"\n\n\t")
	)

builder_region = (
	input(
		"\n" + 
		"Please enter the abbreviation for the region containing " + 
		f"{builder_city} \n" + 
		f"and also currently locates {builder_name} \n" +
		"(e.g. Washington State -> 'WA'):" 
		"\n\n\t")
	)	

builder_country = (
	input(
		"\n" +
		"Please enter the 2-character country code for \n" +
		f"the current location of {builder_name} \n" +
		"(Common examples: USA -> 'US', India -> 'IN'):" +
		"\n\n\t")
	)

# Asking user to create key, ensuring it is 6+ chars

builder_key_input_message = (
		"\n" +
		"Please enter a minimum 6-character key for future signature " +
		"authentication. \n" + 
		"This key will be saved in a local file for automation \n" +
		"so it needs not to be memorized:"
		"\n\n\t") 

builder_key = input(builder_key_input_message)

while len(builder_key) < 6:
	print("\n" +
		f"'{builder_key}' is not a valid key, as it is less than 6 " +
		"characters long. \n"
	)
	builder_key = input(builder_key_input_message)
	 
builder_signature_display = (
	"\n" + 
	f"{builder_name} | {builder_company} - {builder_department} \n" +
	f"{builder_city}, {builder_region}, {builder_country} \n" +
	f"(Auth key = {builder_key}) \n"	
	)

# Displaying new signature to user and asking if new signature can be saved

print(
	"\n" +
	"The following signature has been created: \n" + 
	builder_signature_display)
					
builder_confirm_message = (
	"\n" + 
	"Please confirm that this signature will be saved locally as \n" +
	"'signature_details.txt' (y/n):"
	"\n\n\t")

builder_confirm = input(builder_confirm_message)

while not (builder_confirm == 'y' or builder_confirm == 'n'):
	print(
		"\n" + 
		f"'{builder_confirm}' is not a valid input. \n")
	builder_confirm = input(builder_confirm_message)
	
if builder_confirm == 'n':
	print(
		"\n" + 
		"Confirmation rejected, local file 'signature_details.txt'\n" + 
		"was not created/modified. \n"
	)
	exit()

# 'w' mode will overwrite file if it exists

with open('signature_details.txt', 'w') as file:
	file.write(
		f"{builder_key}\n" +
		f"{builder_key}\n" +
		f"{builder_name}\n" +
		f"{builder_department}\n" +
		f"{builder_company}\n" +
		f"{builder_city}\n" +	
		f"{builder_region}\n" +	
		f"{builder_country}\n" +
		"yes"
	)	

print(
	"\n" +
	"Signature saved successfully to local file 'signature_details.txt'\n"
)

