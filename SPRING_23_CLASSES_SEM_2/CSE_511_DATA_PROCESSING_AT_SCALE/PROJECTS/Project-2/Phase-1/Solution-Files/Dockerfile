
FROM ubuntu:22.04

# ARGs
# https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG TARGETPLATFORM=linux/amd64,linux/arm64
ARG DEBIAN_FRONTEND=noninteractive

# neo4j 5.5.0 installation and some cleanup
RUN apt-get update && \
    apt-get install -y wget gnupg software-properties-common && \
    wget -O - https://debian.neo4j.com/neotechnology.gpg.key | apt-key add - && \
    echo 'deb https://debian.neo4j.com stable latest' > /etc/apt/sources.list.d/neo4j.list && \
    add-apt-repository universe && \
    apt-get update && \
    apt-get install -y nano unzip neo4j=1:5.5.0 python3-pip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# TODO: Complete the Dockerfile

RUN mkdir /cse511
RUN apt-get update && apt-get install -y git

ENV GITHUB_TOKEN=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
ENV USERNAME=ameygoes
RUN git clone https://oauth2:${GITHUB_TOKEN}@github.com/CSE511-SPRING-2023/abhilega-project-2.git  /cse511

WORKDIR /cse511

RUN wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-03.parquet 

WORKDIR /cse511

RUN sed -i 's/#server.default_listen_address=0.0.0.0/server.default_listen_address=0.0.0.0/g' /etc/neo4j/neo4j.conf
RUN neo4j-admin dbms set-initial-password project2phase1


RUN python3 -m pip install --upgrade pip
RUN pip install pandas
RUN pip install neo4j
RUN pip install pyarrow

RUN  wget  https://graphdatascience.ninja/neo4j-graph-data-science-2.3.1.zip 
RUN unzip neo4j-graph-data-science-2.3.1.zip
RUN mv neo4j-graph-data-science-2.3.1.jar /var/lib/neo4j/plugins/

RUN sed -i 's/#server.default_listen_address=0.0.0.0/server.default_listen_address=0.0.0.0/g' /etc/neo4j/neo4j.conf
RUN sed -i '$a dbms.security.procedures.unrestricted=gds.*' /etc/neo4j/neo4j.conf
RUN	sed -i '$a dbms.security.procedures.allowlist=gds.*' /etc/neo4j/neo4j.conf

# Run the data loader script
RUN chmod +x /cse511/data_loader.py && \
    neo4j start && \
    python3 data_loader.py && \
    neo4j stop

# Expose neo4j ports
EXPOSE 7474 7687

# Start neo4j service and show the logs on container run
CMD ["/bin/bash", "-c", "neo4j start && tail -f /dev/null"]
