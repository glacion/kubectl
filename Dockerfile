FROM debian:buster-slim

ARG version
ARG build_date
ARG revision

LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.authors="Ahmetcan Güvendiren <ahmtcngvndrn@gmail.com>"
LABEL org.opencontainers.image.created=${build_date}
LABEL org.opencontainers.image.url="https://github.com/glacion/kubectl"
LABEL org.opencontainers.image.documentation="https://github.com/glacion/kubectl"
LABEL org.opencontainers.image.source="https://github.com/glacion/kubectl"
LABEL org.opencontainers.image.version=${version}
LABEL org.opencontainers.image.revision=${revision}
LABEL org.opencontainers.image.vendor="Ahmetcan Güvendiren <ahmtcngvndrn@gmail.com>"
LABEL org.opencontainers.image.title="kubectl"
LABEL org.opencontainers.image.description="image that contains kubectl, make, envsubst, and curl"

ENV VERSION=${version}

WORKDIR /root

RUN apt update
RUN apt install --no-install-recommends --yes gettext-base make curl ca-certificates 
RUN curl --location \
    --fail \
    -o /usr/local/bin/kubectl \
    "https://storage.googleapis.com/kubernetes-release/release/${VERSION}/bin/linux/amd64/kubectl"

RUN chmod +x /usr/local/bin/kubectl
RUN rm -rf /var/lib/apt /var/cache
