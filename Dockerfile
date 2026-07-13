FROM homebrew/brew:master
USER root

# 	REQUIREMENTS FOR INSTALLING SCRIPT DEPENDENCIES

RUN apt-get -y update
RUN apt-get install -y openjdk-17-jdk
RUN apt-get install -y openjdk-17-jre
RUN apt-get install -y ncat

# Execute next commands in the directory /workspace

WORKDIR /workspace

# SCRIPT DEPENDENCIES

COPY github_PA_token.txt .
RUN	brew install gh -q && \
	gh auth login --with-token < github_PA_token.txt 


# SETTING UP ANDROID SDK BUILD AND COMMAND LINE TOOLS VIA SDK MANAGER

COPY commandlinetools-linux.zip .
COPY local-dependencies ./local-dependencies

RUN	unzip commandlinetools-linux.zip -d sdk

RUN	cd sdk && \ 
	mv cmdline-tools latest && \ 
	mkdir cmdline-tools && \ 
	mv latest cmdline-tools/latest && \ 
	cd .. 

RUN	ln -s sdk/cmdline-tools/latest/bin/sdkmanager ./sdkmanager && \
	echo y | ./sdkmanager --install "build-tools;37.0.0"  && \
	rm sdkmanager && \

	mv sdk local-dependencies/sdk


COPY local.properties .
COPY signature_details.txt .

# PREPPING SHELL SCRIPT

COPY auto_deployer.sh .
RUN chmod +x ./auto_deployer.sh

# Run the script when starting the container
CMD [ "./auto_deployer.sh" ]
