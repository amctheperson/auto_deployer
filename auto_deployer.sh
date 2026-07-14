#!/bin/bash

printf "\nAUTO DEPLOYER 2026\n\n"

printf "\t[1/8] Linking TestApp repo and private files...\n"

# Symbolic links of project files to current directory (required to have gradle work properly while calling it from a separate directory)

ln -s TestApp/* .
ln -s local-dependencies/* .

#	=== Compiling APK for release ==

# Build unsigned APK with Gradle

printf "\t[2/8] Assembling unsigned APK..\n"

#TestApp/gradlew assemble
TestApp/gradlew assemble >/dev/null


# Generate keystore Java file (if non-existent)

if ! [ -f quick-release-key.jks ]
then	
	printf "\t[3/8] Generating keystore file...\n"

	keytool -genkey -keystore quick-release-key.jks \
	-keyalg RSA -keysize 2048 -validity 10000 \
	-alias andrewc < signature_details.txt \
	2>/dev/null
else
	printf "\t[3/8] Existing keystore file located...\n" 
fi


# Symbolic links for zipalign and apksigner, releases folder too
# For ease of implementation, removed at end of script to avoid clutter

ln -s local-dependencies/sdk/build-tools/37.0.0/apksigner ./apksigner
ln -s local-dependencies/sdk/build-tools/37.0.0/zipalign ./zipalign

ln -s TestApp/app/build/outputs/apk/release/ ./


# Align APK files (required before signing APK file)

printf "\t[4/8] Aligning uncompressed APK files for storage optimization..\n"

./zipalign -P 16 -f 4 release/app-release-unsigned.apk \
release/app-release-unsigned-but-its-aligned.apk


# ./zipalign -P 16 -f 4 release/app-release-unsigned.apk \
# release/app-release-unsigned-but-its-aligned.apk 2>/dev/null


# Sign APK with keystore Java file

printf "\t[5/8] Signing aligned APK..\n"

./apksigner sign --ks quick-release-key.jks \
--out release/app-release-signed.apk \
release/app-release-unsigned-but-its-aligned.apk <<< "123123" 1>/dev/null

# Removing symbolic links and intermediate apk files

rm ./zipalign ./apksigner ./release/app-release-unsigned.apk release/app-release-unsigned-but-its-aligned.apk ./release


printf "\t[6/8] Signed APK file created successfully. File location:\n\t\t TestApp/app/build/outputs/apk/release/app-release-signed.apk\n"

cd TestApp

#	=== Uploading release to GitHub repo ===

# Establishing symbolic links for convenience (and readability)

ln -s app/build/outputs/apk/release/app-release-signed.apk

# Get current commit hash of master branch of repo
# aka most recently committed hash

most_recent_commit_hash=$(git rev-parse origin/master)


# Getting info on most recently committed hash
# --no-patch flag removes diff info
# --format option used to return only the email subject (message) of the commit

new_release_title=$(git show --format="%s" --no-patch "$most_recent_commit_hash")   
new_release_notes_file="release-notes.txt"


# release tag defaults to initial release version
tag=v0.1

printf "\t[7/8] "

# Check if any repo releases exist

result=$(gh release view 2>&1)
if [ "$result" = "release not found" ]; then

	printf "Uploading initial release to repo..\n"

else
	printf "Uploading new release to repo..\n"

	# gh release used to get info on latest release on repo
	# --json option used to get JSON string with tagName field
	# --jq option used also to filter said JSON string to just
	# the single entry

	curVersion=$(gh release view --json tagName --jq '.tagName')
	newVersion=""

	# For this proof-of-concept we can assume
	# that this auto-deploy pipeline is for minor updates
	# rather than major updates

	# Therefore release version numbers will never "round up majorly"
	# like 0.9 -> 1.0

	# Thus for new version numbers we can take the old version number
	# and append a "1" if last num is 9
	# otherwise increase last digit by 1
	# like 0.9 -> 0.91 or 2.3 -> 2.4

	if [ ${curVersion:(-1)} = "9" ]; then
 
		newVersion="${curVersion}1" 
	else    
		# curVersion substring that is full string - the final char

		prefix=${curVersion:0:$((${#curVersion}-1))} 
	 
		# Increments final char of curVersion as int
 
		suffix=$((${curVersion:(-1)}+1)) 
	 
		newVersion="${prefix}${suffix}"

		tag=$newVersion
	fi
fi

new_link=$(gh release create $tag --latest --notes-file "$new_release_notes_file" --title "$new_release_title" app-release-signed.apk)

printf "\t[8/8] Release uploaded to GitHub repo. Page link:\n\t\t$new_link\n"

# Removing established symbolic links inside repo directory 
rm app-release-signed.apk

# Removing established symbolic links in auto_deployer folder from repo
cd ..
rm $(ls TestApp)
rm -rf TestApp

# Testing commands

# Removing releases

#clear init release
#gh release delete v0.1 -y --cleanup-tag

ncat -l 8080
