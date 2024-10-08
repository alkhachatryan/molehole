import re

import socketio
import eventlet.wsgi
from flask import Flask
from dotenv import load_dotenv
from enums.status_enum import StatusEnum
import os
import subprocess

env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path=env_path)

sio = socketio.Server(async_mode='eventlet')
app = Flask(__name__)
app = socketio.WSGIApp(sio, app)

active_connections = {}

def run_command(sid, command):
    cd_pattern = r'^cd\s+(.+)$'

    cd_command = re.match(cd_pattern, command)
    if cd_command:
        try:
            new_path = cd_command.group(1).replace('\n', '')
            result = subprocess.run(
                'pwd',
                capture_output=True,
                text=True,
                shell=True,
                executable=active_connections[sid]['executable'],
                cwd=new_path
            )
            new_path = result.stdout if result.stdout else result.stderr
            active_connections[sid]['state']['current_path'] = new_path.replace('\n', '')
            return ''
        except Exception as e:
            return str(e)

    elif is_interactive_command(command):
        return 'interactive commands are disallowed'

    try:
        result = subprocess.run(
            command.replace('\n', ''),
            capture_output=True,
            text=True,
            shell=True,
            executable=active_connections[sid]['executable'],
            cwd=active_connections[sid]['state']['current_path']
        )

        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return str(e)

def is_interactive_command(command):
    interactive_commands = [
        "nano", "vim", "vi", "emacs", "gedit", "kate",
        "bash", "sh", "zsh", "fish", "tcsh", "csh", "ksh",
        "mc", "ranger", "vifm", "nmtui", "lf",
        "htop", "top", "atop", "glances", "nmon",
        "tail", "less", "more", "watch", "dstat",
        "iftop", "nload", "tcpdump", "wireshark", "sftp", "ftp", "ssh", "telnet", "nmcli",
        "mysql", "psql", "sqlite3", "redis-cli",
        "aptitude", "dpkg-reconfigure",
        "git", "tig",
        "alsamixer", "alsactl", "fsck", "passwd", "visudo", "fdisk", "parted", "cfdisk", "gparted", "blkid",
        "duf", "ncdu", "gdisk", "adduser", "usermod", "chpasswd",
        "gdb", "strace", "ltrace", "valgrind", "python", "node", "irb",
        "man", "info", "dialog", "zenity", "whiptail", "cryptsetup", "sysctl", "grub-install", "ddrescue",
        "docker", "lxc", "virsh",
        "make", "cmake", "configure",
        "dd", "mkfs", "7z", "unzip", "tar", "zip"
    ]

    first_part = command.split()[0] if command else ''

    # Check if the command matches an interactive command
    for interactive_command in interactive_commands:
        if first_part.startswith(interactive_command):
            return True

    return False


def set_executable(sid):
    bash_path = subprocess.run(
        ["which", "bash"],
        capture_output=True,
        text=True
    )

    active_connections[sid]['executable'] = bash_path.stdout.strip()

def set_current_path(sid):
    result = subprocess.run(
        'pwd',
        capture_output=True,
        text=True,
        shell=True,
        executable=active_connections[sid]['executable']
    )

    current_path = result.stdout if result.stdout else result.stderr
    active_connections[sid]['state']['current_path'] = current_path.replace('\n', '')


def init_connection(sid):
    active_connections[sid] = {
        'state': {},
        'executable': None,
    }

@sio.event
def connect(sid, environ, auth):
    if auth and auth.get('token') == os.getenv('AUTH_TOKEN'):
        init_connection(sid)
        set_executable(sid)
        set_current_path(sid)

        sio.emit('status', {
            'status': StatusEnum.SUCCESSFUL_CONNECTION,
            'state': active_connections[sid]['state'],
        }, to=sid)
    else:
        sio.emit('status', {
            'status': StatusEnum.AUTH_FAILED,
        }, to=sid)
        del active_connections[sid]
        sio.disconnect(sid)

@sio.event
def cmd(sid, command):
    if command is None or command == '':
        sio.emit('command_output', {
            'output': '',
            'state': active_connections[sid]['state'],
        }, to=sid)
        return None


    sio.emit('command_output', {
        'output': run_command(sid, command),
        'state': active_connections[sid]['state'],
    }, to=sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen((os.getenv('SERVER_IP'), int(os.getenv('SERVER_PORT')))), app)
