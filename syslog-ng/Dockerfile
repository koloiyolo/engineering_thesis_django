FROM balabit/syslog-ng:4.6.0

COPY delay.sh /etc/dev/delay.sh
RUN chmod 777 /etc/dev/delay.sh

COPY syslog-ng.conf /etc/syslog-ng/syslog-ng.conf

EXPOSE 514/udp
EXPOSE 601

WORKDIR /etc/syslog-ng

CMD ["-edv"]
