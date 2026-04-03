#!/usr/bin/env python
import os
import re
import subprocess
import sys
import yaml

def run(args, input=None):
  print(f'run: {" ".join(args)}')
  r = subprocess.run(
      args=args,
      input=str.encode(input) if input else None,
      capture_output=True,
      check=True,
      timeout=30)
  return r.stdout

def readtxt(path):
  with open(path, "r") as f:
    return f.read()

def get_config_name(path):
  r = run(['esphome', 'config', path])
  y = yaml.safe_load(r)
  return y['esphome']['name']

def check_input(yaml_path):
  basename = os.path.basename(yaml_path)
  name, extension = os.path.splitext(basename)

  if extension != ".yaml":
    print(f'not a yaml file: {basename}')
    sys.exit(1)

yaml_path = os.path.abspath(sys.argv[1])
check_input(yaml_path)

yaml_dir_path = os.path.dirname(yaml_path)
name = get_config_name(yaml_path)
bin_path = f'{yaml_dir_path}/.esphome/build/{name}/.pioenvs/{name}/program'

if not os.path.exists(bin_path):
  print(f'not found: {bin_path}')
  print('are you in same dir as when you ran `esphome compile`?')
  sys.exit(1)
print(f'found binary: {bin_path}')

service_name = f'esphome-{name}'
service_file = f'/etc/systemd/system/{service_name}.service'
print(f'systemd service file: {service_file}')

opt_dir = f'/opt/{service_name}'
print(f'opt dir for binary: {opt_dir}')

extra_service = ''
extra_service_path = f'{yaml_dir_path}/{name}.extraservice'
if os.path.exists(extra_service_path):
  extra_service = readtxt(extra_service_path)

user_config ="""
DynamicUser=yes
User={service_name}
"""
if re.search(r'^User=', extra_service, re.MULTILINE):
  user_config = ''

service_config = f"""
[Unit]
Description={service_name}
After=network.target

[Service]
Environment="PATH=/usr/bin:/bin" "SHELL=/usr/bin/zsh" "HOME=/tmp"
Type=simple
{user_config}
PrivateTmp=true
ExecStart={opt_dir}/{name}
Restart=always
RestartSec=60
KillSignal=SIGINT
TimeoutStopSec=30
{extra_service}

[Install]
WantedBy=multi-user.target
"""

run(['sudo', 'mkdir', '-p', opt_dir])

opt_bin_path = f'{opt_dir}/{name}'
if os.path.exists(opt_bin_path):
  # can not overwrite binary if its running
  run(['sudo', 'rm', opt_bin_path])
run(['sudo', 'cp', bin_path, opt_bin_path])

run(['sudo', 'tee', service_file], service_config)
run(['sudo', 'systemctl', 'daemon-reload'])
run(['sudo', 'systemctl', 'enable', service_name])
run(['sudo', 'systemctl', 'restart', service_name])
