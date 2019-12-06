FROM amazonlinux:latest
RUN yum install -y python3-pip git zip
CMD /src/package.sh
