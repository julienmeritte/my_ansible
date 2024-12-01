import os

from modules.base_module import BaseModule
import modules.log_module as logModule
import paramiko


class CopyModule(BaseModule):
    bastion_host: str = "127.0.0.1"
    bastion_port: int = 22
    bastion_username: str = "bob"
    bastion_password: str = ""

    def __init__(self, inventory):
        super().__init__()
        self.name = "COPY"
        try:
            host = inventory['hosts']['webserver']['ssh_address']
            port = inventory['hosts']['webserver']['ssh_port']
            self.host = host
            self.port = port

        except KeyError:
            logModule.debug_log("Failed to retrieve keys from inventory")
        try:
            username = inventory['hosts']['webserver']['ssh_username']
            password = inventory['hosts']['webserver']['ssh_password']
            self.username = username
            self.password = password
        except KeyError:
            logModule.debug_log("No valid username/password valid for webserver ssh")

        try:
            bastion_host = inventory['hosts']['bastion']['ssh_address']
            bastion_port = inventory['hosts']['bastion']['ssh_port']
            self.bastion_host = bastion_host
            self.bastion_port = bastion_port

        except KeyError:
            logModule.debug_log("Failed to retrieve keys from inventory")
        try:
            bastion_username = inventory['hosts']['bastion']['ssh_username']
            bastion_password = inventory['hosts']['bastion']['ssh_password']
            self.bastion_username = bastion_username
            self.bastion_password = bastion_password
        except KeyError:
            logModule.debug_log("No valid username/password valid for webserver ssh")

    def execute_sftp_copy(self, src, dest):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.bastion_host, port=self.bastion_port, username=self.bastion_username,
                    password=self.bastion_password, timeout=3)

        ftp_client = ssh.open_sftp()
        local_temp_path = os.path.abspath("./temp/" + os.path.basename(src))
        if os.name == 'nt':
            local_temp_path = local_temp_path.replace('\\', '\\\\')
        ftp_client.get(src, local_temp_path)
        ftp_client.close()

        ssh.connect(self.host, port=self.port, username=self.username,
                    password=self.password, timeout=3)

        ftp_client = ssh.open_sftp()
        ftp_client.put(local_temp_path, dest)
        ftp_client.close()

        if os.path.exists(local_temp_path):
            os.remove(local_temp_path)
