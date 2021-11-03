FROM ubuntu:18.04
LABEL Maintainer="Sean Jungbluth, sjungbluth@lbl.gov" Version=1.0

RUN apt-get -y -m update && apt-get install -y -qq python3 tzdata 
RUN apt-get -y install build-essential git gcc-multilib apt-utils expat libexpat-dev wget perl cpanminus libnet-ssleay-perl python3-pandas

RUN perl -MNet::FTP -e '$ftp = new Net::FTP("ftp.ncbi.nlm.nih.gov", Passive => 1); $ftp->login; $ftp->binary; $ftp->get("/entrez/entrezdirect/edirect.tar.gz");'

RUN gunzip -c edirect.tar.gz | tar xf - && rm edirect.tar.gz
RUN cpanm HTML::Entities
RUN cpanm XML::Simple
RUN cpanm IO::Socket::SSL
RUN cpanm LWP::Protocol::https
RUN cpanm HTML::Entities

RUN wget https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/xtract.Linux.gz && gunzip xtract.Linux.gz && mv xtract.Linux /edirect/xtract && chmod +x /edirect/xtract

RUN echo "B"

RUN git clone https://github.com/jungbluth/taxonomy_welder

ENV PATH="/edirect:${PATH}"
WORKDIR "/taxonomy_welder"
