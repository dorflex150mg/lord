"""
Build script for Lord. 
Installs and runs rabbitmq
"""
import subprocess

args1 = ["sudo", "apt-get", "-y", "install", "rabbitmq-server"]
subprocess.call(args1)
args2 = ["sudo", "systemctl", "enable", "rabbitmq-server"]
subprocess.call(args2)
args3 = ["sudo", "systemctl", "start", "rabbitmq-server"]
subprocess.call(args3)
args4 = ["pip", "install", "pika"]
subprocess.call(args4)
args5 = ["pip", "install", "msgpack"]
subprocess.call(args5)
