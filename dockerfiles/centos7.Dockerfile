FROM centos:7

ENV FTP_USER=1002
ENV FTP_GROUP=1002

RUN yum install -y openssh-server python3 && \
    groupadd -g ${FTP_GROUP} sftp_user && \
    mkdir -p /app/sftp && \
    mkdir -p /app/sftp/in /app/sftp/out && \
    useradd -rm -d /app/sftp -g ${FTP_GROUP} -u ${FTP_USER} sftp_user && \
    echo "sftp_user:example" | chpasswd && \
    /usr/bin/ssh-keygen -A && \
    chown -R sftp_user:sftp_user /app/sftp && \
    chmod -R 700 /app/sftp && \
    printf 'Match User sftp_user \n\
ForceCommand internal-sftp \n\
PasswordAuthentication yes \n\
ChrootDirectory /app/sftp \n\
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
