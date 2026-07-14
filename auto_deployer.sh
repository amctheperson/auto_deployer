#!/bin/bash

: '
AUTO DEPLOYER 2026
PAGE 0




	Table of Contents

	-----------------------------------------------------------------

	Building an Unsigned APK with Gradle				1

	Aligning and Signing APK with Android SDK Build Tools		2

	Retrieving Info on New Release via Latest Push to Master	3

	Determining New Release Version Number Algorithmically		4
	
	Upload New Release on GitHub Repo with Obtained Release Info	5

	Script Clean-up / Cloud Run Service Requirement			6




	File Description


	This Bash script builds an APK file, signs it, and deploys the file
	on the same GitHub repo the APK file was retrieved from.
	
'





















#								 1 : CTRL + F ->


: '
AUTO DEPLOYER 2026
PAGE 1

Building an unsigned APK with Gradle
'


printf "\nAUTO DEPLOYER 2026\n\n"

printf "\t[1/3] Building unsigned APK..\n"

# Symbolic links for convenience / avoiding refactoring
# and for Gradle to work properly since it's in a different directory

ln -s TestApp/* .
ln -s local-dependencies/* .

TestApp/gradlew assemble >/dev/null



































# <- 0 : CTRL + B						 2 : CTRL + F ->


: '
AUTO DEPLOYER 2026
PAGE 2

Aligning and Signing APK with Android SDK Build Tools
'
	# Aligning uncompressed APK files is done for storage optimization

	# APK files need a signature of whomever assembled it before it can be
	installable


printf "\t[2/3] Aligning and signing APK file..\n"

# Generate signature file (if non-existent) from signature details text file 

if ! [ -f quick-release-key.jks ]
then	
	keytool -genkey -keystore quick-release-key.jks \
	-keyalg RSA -keysize 2048 -validity 10000 \
	-alias andrewc < signature_details.txt \
	2>/dev/null
fi


# Symbolic links for relevant build tools and folder where APKs are generated

ln -s local-dependencies/sdk/build-tools/37.0.0/apksigner ./apksigner
ln -s local-dependencies/sdk/build-tools/37.0.0/zipalign ./zipalign

ln -s TestApp/app/build/outputs/apk/release/ ./

# Align unsigned APK

./zipalign -P 16 -f 4 release/app-release-unsigned.apk \
release/app-release-unsigned-but-its-aligned.apk 2>/dev/null

# Sign aligned but unsigned APK with signature file (keystore Java file, .jks)

./apksigner sign --ks quick-release-key.jks \
--out release/app-release-signed.apk \
release/app-release-unsigned-but-its-aligned.apk <<< "123123" 1>/dev/null


# Removing symbolic links and intermediate apk file

rm ./zipalign ./apksigner ./release/app-release-unsigned.apk release/app-release-unsigned-but-its-aligned.apk ./release


printf "\n\tSigned APK file created successfully. File location:\n\t\t TestApp/app/build/outputs/apk/release/app-release-signed.apk\n"


# <- 1 : CTRL + B						 3 : CTRL + F ->


: '
AUTO DEPLOYER 2026
PAGE 3

Retrieving Info on New Release via Latest Push to Master
'

printf "\t[3/3] "

# Working with GitHub repo requires calls from valid repo directory
cd TestApp

# Quick access to release file location
ln -s app/build/outputs/apk/release/app-release-signed.apk


# Get the current commit hashcode of master branch of repo aka
# Get most recently committed hash to master

most_recent_commit_hash=$(git rev-parse origin/master)

# Get relevant info on most recently committed hash

# --no-patch flag removes diff info
# --format option used to return only the email subject (message) of the commit

new_release_title=$(git show --format="%s" --no-patch "$most_recent_commit_hash")   
new_release_notes_file="release-notes.txt"

























# <- 1 : CTRL + B						 3 : CTRL + F ->


: '
AUTO DEPLOYER 2026
PAGE 4

Determining New Release Version Number Algorithmically
'
	# For now we assume that this auto-deploy pipeline
	# is for minor updates only 

	# Therefore release version numbers will never round up any digits
	# larger than the last one (representing a major update)
	# aka v0.9 - X -> 1.0 , v0.9 -> v0.91

	# Thus for new version numbers we just increase the last digit by 1
	# unless the last digit is a 9 then we just append a 1 instead
	# like 2.3 -> 2.4, or 1.99 -> 1.991


# release tag defaults to initial release version
tag=v0.1

# Check if any repo releases exist

result=$(gh release view 2>&1)
if [ "$result" = "release not found" ]; then

	printf "Uploading initial release to repo..\n"

else
	printf "Uploading new release to repo..\n"

	# Get info on latest release on repo
	# --json option used to get JSON string containing tagName field
	# --jq option used to filter said JSON string to just the single entry

	curVersion=$(gh release view --json tagName --jq '.tagName')
	newVersion=""

	if [ ${curVersion:(-1)} = "9" ]; then
 
		newVersion="${curVersion}1" 
	else    
		# curVersion substring that is full string except the final char
		prefix=${curVersion:0:$((${#curVersion}-1))} 
	 
		# Increments final char of curVersion as int 
		suffix=$((${curVersion:(-1)}+1)) 
	 
		newVersion="${prefix}${suffix}"

		tag=$newVersion
	fi
fi

# <- 3 : CTRL + B						 5 : CTRL + F ->


: '
AUTO DEPLOYER 2026
PAGE 5

Upload New Release on GitHub Repo with Obtained Release Info
'


new_link=$(gh release create $tag \
	--latest \
	--notes-file "$new_release_notes_file" \
	--title "$new_release_title" \
	app-release-signed.apk)

printf "\n\tRelease uploaded to GitHub repo. Page link:\n\t\t$new_link\n"







































# <- 4 : CTRL + B						 6 : CTRL + F ->


: '
AUTO DEPLOYER 2026
PAGE 6

Script clean-up / Cloud Run Service Requirement
'


# Cleaning up repo directory 

rm app-release-signed.apk

# Cleaning up auto_deployer folder from repo

cd ..
rm $(ls TestApp)
rm -rf TestApp


# Script testing command artifact
# Left behind for demo

# Removing releases

#clear init release
#gh release delete v0.1 -y --cleanup-tag


# Cloud Run Service requires that service listens to port 8080 on TCP

ncat -l 8080























# <- 5 : CTRL + B 

