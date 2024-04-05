FROM postgres:15-alpine

LABEL maintainer="Just van den Broecke <justb4@gmail.com>"
 
RUN apk add --no-cache --update gettext python3 py3-click py3-docker-py && mkdir /pgbackup

ENV PGB_SCHEDULE 0 23 * * *

ADD docker/* /pgbackup/

CMD ["/pgbackup/entrypoint.sh"]
