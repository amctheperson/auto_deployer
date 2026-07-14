

#			AUTO_DEPLOYER 2026 DOCKERFILE

#	Note: This Dockerfile should be in the same directory as the GitHub repo
#	that triggers a Cloud Build -> Cloud Run

#	Base image: Ubuntu with HomeBrew installed - for convenience
#	Root acess user may be implied already TODO

FROM 	homebrew/brew:master
USER 	root

# 	All following commands executed in /workspace directory

WORKDIR /workspace

RUN 	apt-get -y update

#				PACKAGE DEPENDENCIES

#	ncat, Linux tool for TCP communication 
#	Google Cloud Run requirement

RUN	apt-get install -y ncat

#	JDK (Java)
#	Required to compile app source code into releasable APK
	
RUN 	apt-get install -y openjdk-17-jdk && \
	apt-get install -y openjdk-17-jre

#			MANUAL DEPENDENCIES

#	Adding Android application source files to container

RUN	git clone https://github.com/amctheperson/TestApp -q

#	Adding executable auto-deployment bash script to container
	
RUN	git clone https://github.com/amctheperson/auto_deployer -q && \
	rm auto_deployer/Dockerfile && \
	mv auto_deployer/* . && \
	chmod +x ./auto_deployer.sh && \
	rm -rf auto_deployer

#	Adding local files for bash script that are technically sensitive
 
COPY	local-dependencies/* ./local-dependencies/

#	TESTING RN

#	Android SDK Build Tools Installation 
#	also a Gradle requirement

	# Retrieving command-line tools via zip hosted on my Google Drive
	 
	# (Quick solution to host large file on Drive 
	# instead of trying to curl the third link on Android Studio's website)
 
RUN	apt-get install -y pipx && \
	pipx ensurepath && \
	pipx run gdown https://drive.google.com/file/d/1XjTqN58f65WP4Kp-c-HNg-zydx9Er3cO/view?usp=sharing -O commandlinetools-linux.zip
	

COPY 	commandlinetools-linux.zip .
RUN	unzip commandlinetools-linux.zip -d sdk

	# Reorganizing sdk directory to format expected by SDK Manager

RUN	cd sdk && \ 
	mv cmdline-tools latest && \ 
	mkdir cmdline-tools && \ 
	mv latest cmdline-tools/latest && \ 
	cd .. 

	# Retrieving build tools via SDK Manager
	
RUN	ln -s sdk/cmdline-tools/latest/bin/sdkmanager ./sdkmanager && \
	echo y | ./sdkmanager --install "build-tools;37.0.0"  && \
	rm sdkmanager && \

	mv sdk local-dependencies/sdk

#			REQUIREMENTS

# 	REQUIREMENTS FOR INSTALLING SCRIPT DEPENDENCIES





# 				SCRIPT DEPENDENCIES

# 	GitHub CLI (gh) Installation and Authentication

#	Used in script for repo release management	

COPY 	auto_deployer/github_PA_token.txt .
RUN	brew install gh -q && \
	gh auth login --with-token < auto_deployer/github_PA_token.txt 




# Run the script when starting the container
CMD [ "./auto_deployer.sh" ]
