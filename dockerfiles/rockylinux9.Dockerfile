FROM rockylinux:9

ENV FTP_USER=1002
ENV FTP_GROUP=1002

RUN yum install -y openssh-server python3 && \
    rm -f /var/run/nologin /etc/nologin && \
    groupadd -g ${FTP_GROUP} sftp_user && \
    mkdir -p /app/transfer/sftp/in /app/transfer/sftp/out && \
    useradd -rm -d /app/transfer/sftp -g ${FTP_GROUP} -u ${FTP_USER} sftp_user && \
    echo "sftp_user:example" | chpasswd && \
    /usr/bin/ssh-keygen -A && \
    chown -R sftp_user:sftp_user /app/transfer/sftp && \
    chmod -R 755 /app/ && \
    printf 'Match User sftp_user \n\
ForceCommand internal-sftp \n\
PasswordAuthentication yes \n\
ChrootDirectory /app/transfer/ \n\
PermitTunnel no  \n\
AllowAgentForwarding no \n\
AllowTcpForwarding no \n\
X11Forwarding no \n' >> /etc/ssh/sshd_config

COPY outputfiles /app/outputfiles
COPY main.py /app/
COPY config.json /app/
COPY --chmod=777 run.sh /app/

EXPOSE 22
CMD ["/app/run.sh"]
