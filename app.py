import modules.log_module as logModule
import logging
import click
import yaml
from modules.configs.constants import *
from modules.apt_module import AptModule
from modules.copy_module import CopyModule
from modules.service_module import ServiceModule
from modules.command_module import CommandModule


@click.command()
@click.option('-f', default="", help='Path to playbooks yaml file.')
@click.option('--debug', is_flag=True, help='Shows all logs on default output')
@click.option('--dry-run', is_flag=True, help='Does not execute commands, write what it would do instead')
def main(f, debug, dry_run):
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
    if not debug:
        logging.getLogger("paramiko").setLevel(logging.WARNING)
    loaded_inventory = load_inventory()
    loaded_playbooks = load_playbooks(f)
    execute_playbooks(loaded_playbooks, loaded_inventory, dry_run)


def execute_playbooks(playbooks, inventory, dry_run):
    for playbook in playbooks:
        if playbook['module'] == 'apt':
            execute_apt_module(playbook, inventory, dry_run)
        elif playbook['module'] == 'copy':
            execute_copy_module(playbook, inventory, dry_run)
        elif playbook['module'] == 'service':
            execute_service_module(playbook, inventory, dry_run)
        elif playbook['module'] == "command":
            execute_command_module(playbook, inventory, dry_run)


def execute_command_module(playbook, inventory, dry_run):
    commandModule = CommandModule(inventory)
    command: str = ""
    try:
        command = playbook['params']['command']
    except KeyError:
        logModule.debug_log("Unable to retrieve command property")

    if command:
        logModule.info_log("Executing following commands : " + command)
        if not dry_run and commandModule.execute_ssh_command(command):
            logModule.info_log("Commands successfully executed.")


def execute_service_module(playbook, inventory, dry_run):
    serviceModule = ServiceModule(inventory)
    service_name: str = ""
    service_state: str = ""
    try:
        service_name = playbook['params']['name']
        service_state = playbook['params']['state']
    except KeyError:
        logModule.debug_log("Unable to retrieve src and dest properties")

    if service_name and service_state:
        serviceModule.execute_service_command(service_name, service_state, dry_run)


def execute_copy_module(playbook, inventory):
    copyModule = CopyModule(inventory)
    copy_src: str = ""
    copy_dest: str = ""
    copy_backup: bool = False
    try:
        copy_src = playbook['params']['src']
        copy_dest = playbook['params']['dest']
    except KeyError:
        logModule.debug_log("Unable to retrieve src and dest properties")

    try:
        copy_backup = playbook['params']['backup']
    except KeyError:
        copy_backup = False
        logModule.debug_log("Unable to retrieve backup property")

    if copy_src and copy_dest:
        copyModule.execute_sftp_copy(copy_src, copy_dest)


def execute_apt_module(playbook, inventory, dry_run):
    aptModule = AptModule(inventory)
    apt_package_name: str = ""
    apt_package_state: str = ""

    try:
        apt_package_name = playbook['params']['name']
        apt_package_state = playbook['params']['state']
    except KeyError:
        logModule.debug_log("Unable to retrieve apt package name")

    if apt_package_name and apt_package_state:
        if apt_package_state == "present":
            logModule.info_log("Installing following package : " + apt_package_name)
            if not dry_run:
                aptModule.execute_ssh_command("sudo -S -p '' apt-get install -y " + apt_package_name)
        elif apt_package_state == "absent":
            logModule.info_log("Uninstalling following package : " + apt_package_name)
            if not dry_run:
                aptModule.execute_ssh_command("sudo -S -p '' apt-get purge --auto-remove -y " + apt_package_name)
    else:
        logModule.debug_log("Apk package not set")


def load_inventory():
    with open(BASE_CONFIG_INVENTORY_PATH) as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logModule.debug_log(exc)


def load_playbooks(f):
    if f:
        playbook_path = "configs/" + f
    else:
        playbook_path = BASE_CONFIG_PLAYBOOKS_PATH

    with open(playbook_path) as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logModule.debug_log(exc)


if __name__ == "__main__":
    main()
