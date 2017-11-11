#!/usr/bin/env python

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
import sys
import argparse

parser=argparse.ArgumentParser(
    description='''Deployment panda services with Ansible ''',
    epilog="""More information in https://github.com/doralteres/panda""")
parser.add_argument('-s', help='Service name to install - img-panda or smart-panda  |   ''all'' will install all the services')
args=parser.parse_args()
if ((args.s != "img-panda")&(args.s != "smart-panda")&(args.s != "all")):
    print ("WRONG ARGs! (use only img-panda or smart-panda or all)")
    sys.exit()

cust_rules = []
cust_rules.append (dict(role="nodejs", tags="nodejs"))
if (args.s != "all"):
    cust_rules.append(dict(role=args.s, tags=args.s))
else:
    cust_rules.append (dict(role="img-panda", tags="img-panda"))
    cust_rules.append (dict(role="smart-panda", tags="smart-panda"))

Options = namedtuple('Options',
                ['connection', 'module_path', 'forks', 'become',
                 'become_method', 'become_user', 'check']
            )

#initialize needed objects
variable_manager = VariableManager()
loader = DataLoader()
options = Options(
    connection='local', module_path='', forks=100, become=True,
    become_method='sudo', become_user='root', check=False)
passwords = dict(vault_pass='secret')

#create inventory and pass to variable manager
inventory = Inventory(loader=loader, variable_manager=variable_manager,
                      host_list='localhost')
variable_manager.set_inventory(inventory)

#create play with tasks
play_src = dict(
    name="Install and run panda services",
    hosts="localhost",
    become="yes",
    roles= cust_rules

)
play = Play().load(play_src, variable_manager=variable_manager, loader=loader)
tqm = None
try:
    tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=passwords,
            stdout_callback="default",
        )
    result = tqm.run(play)
finally:
    if tqm is not None:
        tqm.cleanup()