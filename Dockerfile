FROM amazonlinux
ADD package.sh /tmp/
RUN yum install -y util-linux python27-virtualenv sudo zip aws-cli
CMD /tmp/package.sh
