FROM alpine:latest as build
ENV VERSION 4.8
ADD https://www.languagetool.org/download/LanguageTool-$VERSION.zip /LanguageTool-$VERSION.zip
RUN unzip LanguageTool-$VERSION.zip \
  && rm LanguageTool-$VERSION.zip


FROM openjdk:13-jdk-alpine
ENV VERSION 4.8
COPY --from=build /LanguageTool-$VERSION.zip /LanguageTool-$VERSION.zip
WORKDIR /LanguageTool-$VERSION
CMD ["java", "-cp", "languagetool-server.jar", "org.languagetool.server.HTTPServer", "--port", "8081", "--public" ]
EXPOSE 8081
