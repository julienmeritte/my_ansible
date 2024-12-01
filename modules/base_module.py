import paramiko
import modules.log_module as logModule


class BaseModule:
    name: str = "BASE"

    def __init__(self, host="192.168.1.22", port=22, username="bob", password=""):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def execute_ssh_command(self, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, port=self.port, username=self.username,
                    password=self.password, timeout=3)
        stdin, stdout, stderr = ssh.exec_command(command + " && echo CMD_SUCCESS || echo CMD_FAILED")
        stdin.write(self.password + '\n')
        stdin.flush()
        output = stdout.read().decode('utf-8').rstrip()
        if output.endswith("\nCMD_SUCCESS"):
            logModule.info_log(output.removesuffix('\nCMD_SUCCESS'), self.host)
            return True
        else:
            logModule.debug_log(stderr.read().decode('utf-8').rstrip(), self.host)
        return False
