from modules.base_module import BaseModule
import modules.log_module as logModule


class AptModule(BaseModule):
    def __init__(self, inventory):
        super().__init__()
        self.name = "APT"
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
