FROM ubuntu:latest
RUN apt-get update
RUN apt install -y curl
# getting python
RUN apt install -y python3-pip
RUN apt-get install -y openssh-client


RUN pip install python-openstackclient
RUN apt install -y jq
RUN apt install -y kubernetes


#helm 
RUN curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | tee /usr/share/keyrings/helm.gpg > /dev/null 
RUN apt-get install apt-transport-https --yes
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | tee /etc/apt/sources.list.d/helm-stable-debian.list 
RUN apt-get update 
RUN apt-get install helm


# for fission

RUN OS=$(uname -s | tr '[:upper:]' '[:lower:]')
RUN export FISSION_VERSION='1.20.0'
RUN curl -Lo fission https://github.com/fission/fission/releases/download/v$FISSION_VERSION/fission-v$FISSION_VERSION-$OS-amd64 \
   && chmod +x fission && mv fission /usr/local/bin/


RUN curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
RUN chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg
# This overwrites any existing configuration in /etc/apt/sources.list.d/kubernetes.list
RUN echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | tee /etc/apt/sources.list.d/kubernetes.list
RUN chmod 644 /etc/apt/sources.list.d/kubernetes.list

RUN apt-get update
RUN apt-get install -y kubectl

RUN apt-get install zip