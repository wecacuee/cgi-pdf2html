FROM ubuntu:18.04
ENV TZ America/Los_Angeles
ENV DEBIAN_FRONTEND noninteractive

# make sure sudo is installed to be able to give user sudo access in docker
# Level 1 packages
RUN apt-get update \
 && apt-get install -y \
    python3-pip \
    poppler-utils

RUN mkdir -p /root/code/cgi-pdf2html
COPY . /root/code/cgi-pdf2html
WORKDIR /root/code/cgi-pdf2html

# Need to add a user because CGIHttpServer wants so
# https://stackoverflow.com/questions/11021369/python-cgihttpserver-crashes-with-oserror-errno-13-permission-denied
ARG USER=user
RUN useradd $USER
RUN chown -R $USER /root
USER $USER
RUN chmod 0775 /root/code/cgi-pdf2html/cgi-bin/pdf2html.py
CMD ["python3", "-mhttp.server", "--cgi", "9797"]

