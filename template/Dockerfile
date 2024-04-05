FROM postgres:$POSTGRES_VERSION-alpine

LABEL maintainer="Just van den Broecke <justb4@gmail.com>"
 
# OLD: upto v13 - CHECK - RUN apk add --no-cache --update gettext python3 py3-pip && pip3 install click docker && mkdir /pgbackup
RUN apk add --no-cache --update gettext python3 py3-click py3-docker-py && mkdir /pgbackup

ENV PGB_SCHEDULE 0 23 * * *

ADD docker/* /pgbackup/

CMD ["/pgbackup/entrypoint.sh"]
