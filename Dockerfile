FROM postgres:12.9-alpine
MAINTAINER "Manoj Ravikumar"

RUN mkdir -p "/home/zdata"
RUN chmod -R 777 "/home/zdata"


RUN echo "Setting up environmental variables for POSTGRES"
ENV POSTGRES_PASSWORD=Pass2022#
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=postgres

RUN echo "Setting up volume for POSTGRES"
ENV PGDATA=/var/lib/postgresql/data
RUN chmod -R 777 "/var/lib/postgresql/data"
VOLUME /var/lib/postgresql/data

RUN echo "Setting up starter scripts for POSTGRES"
RUN mkdir -p "/home/sqlscripts"
RUN chmod -R 777 "/home/sqlscripts"
WORKDIR /opt/setup/
RUN chmod -R 777 "/opt/setup"
COPY db-scripts.d/db-setup.sh /opt/setup/
COPY db-scripts.d/db-pack.sh /opt/setup/
COPY db-scripts.d/db-run.sh /opt/setup/
RUN chmod -R 777 "/opt/setup"


USER postgres
COPY init-data/init-db.sql /home/sqlscripts/init-db.sql
RUN ./db-setup.sh && ./db-pack.sh
EXPOSE 5432

ENTRYPOINT "/opt/setup/db-run.sh"

RUN echo "Setting up folders for docker images"
CMD psql -f /home/init-data/init-db.sql

CMD postgres
RUN echo "Done setting up postgres db using dockerfile"
RUN echo "By Manoj Ravikumar - Jesus Loves You"
