FROM amazonlinux:latest
RUN yum -y groupinstall 'Development Tools'
RUN yum -y install libffi-devel openssl-devel python3-pip
CMD /src/package.sh
