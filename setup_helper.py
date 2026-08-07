



"""

			GitHub Personal Access Token Setup

	Page	Purpose

	1	Confirmer function
			


"""






































#					0


#							            CTRL + F -->


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

 















#					1


# <-- CTRL + B							    

