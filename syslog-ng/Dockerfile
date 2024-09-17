FROM balabit/syslog-ng:4.6.0

# Install the MySQL client
RUN apt-get update && apt-get install -y mariadb-client

COPY delay.sh /etc/dev/delay.sh
COPY create_log.sql /etc/dev/create_log.sql
RUN chmod 777 /etc/dev/delay.sh

COPY syslog-ng.conf /etc/syslog-ng/syslog-ng.conf

EXPOSE 514/udp
EXPOSE 601

WORKDIR /etc/syslog-ng

CMD ["-edv"]
