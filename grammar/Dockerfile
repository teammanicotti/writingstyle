FROM alpine:latest

RUN apk update \
  && apk upgrade \
  && apk add --no-cache bash \
  && apk add --no-cache --virtual=build-dependencies unzip \
  && apk add --no-cache openjdk8-jre

ENV VERSION 4.8
ADD https://www.languagetool.org/download/LanguageTool-$VERSION.zip /LanguageTool-$VERSION.zip

RUN unzip LanguageTool-$VERSION.zip \
  && rm LanguageTool-$VERSION.zip

WORKDIR /LanguageTool-$VERSION

CMD ["java", "-cp", "languagetool-server.jar", "org.languagetool.server.HTTPServer", "--port", "8081", "--public" ]
EXPOSE 8081
