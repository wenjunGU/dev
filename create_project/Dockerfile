from golang:1.13

RUN mkdir /opt/resource/models
RUN mkdir /opt/bin
ADD go.mod /opt/resource/

ADD main.go /opt/resource/
ADD main.go /usr/local/go/src/resource/

ADD models /opt/resource/models/
ADD models /usr/local/go/src/resource/models/

WORKDIR /opt/resource
RUN go build -o resource
RUN mv resource /opt/bin

WORKDIR /opt/bin/
