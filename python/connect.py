import sys
import os
import datetime
import time

import paramiko
import crypt
import json
import re
import redis


class SSHConnect:
    name_size_date = "ls -l --full-time | tr -s ' ' | cut -d ' ' -f 9,5,6"
    root_password = '88609723'
    HOME_DIR = '/home'

    def __init__(self):
        transport = paramiko.Transport(('127.0.0.1', 22))
        transport.connect(username='root', password='88609723')
        client = paramiko.SSHClient()
        client._transport = transport
        self.client = client
        self.sftp = paramiko.SFTPClient.from_transport(transport)

    def file_name(self, dir):
        if os.path.exists(dir):
            for file in os.listdir(dir):
                if file[0] is not '.':
                    str = re.sub(' ', '_', file)
                    if str != file:
                        sin, sout, serr = self.client.exec_command('sudo mv ' + file + ' ' +  str)
                        sin.write(self.root_password + '\n')
                    # os.renames(dir + file, dir + str)
        else:
            print('not exist')

    def read_dir(self, dir):
        self.file_name(dir)

        dict = {}
        k = 0
        client = self.client
        stdin, stdout, stderr = client.exec_command('cd ' + dir + ';' + self.name_size_date, timeout=60)

        for temp in stdout:
            if temp == '\n':
                continue

            args = temp.split(' ', 3)
            size = args[0]
            date = args[1]
            filename = args[2][:-1]
            sin, sout, serr = client.exec_command('cd ' + dir + ';file -b -L ' + filename)
            for i in sout:
                type = i.split('\n')[0]

            dict[k] = {
                'type' : type,
                'time' : date,
                'name': filename,
                'size': size
            }

            k = k + 1

        json_str = json.dumps(dict)
        return json_str

    def check_login(self, username, password):
        client = self.client
        root_password = self.root_password
        find_user_file = 'cd ' + self.HOME_DIR +  '; find . -maxdepth 1 -name ' + username
        get_user_password = 'less /etc/shadow | grep ' + username

        stdin, stdout, stderr = client.exec_command(find_user_file, timeout=60)

        for file in stdout:
            if file:
                sin, sout, err = client.exec_command(get_user_password, timeout=60)
                sin.write(root_password + '\n')

                encryption_password = ''
                for line in sout:
                    encryption_password = line.split(':')[1]

                salt = encryption_password.split('/')[0]
                hash_password = crypt.crypt(password, salt)

                if hash_password == encryption_password:
                    return "OK"
                else:
                    return "PasswordError"

            else:
                return "NoUser"

    def signup(self, username, password):
        client = self.client
        root_password = self.root_password
        root_dir = self.HOME_DIR + '/' + username
        add_user = 'sudo useradd ' + username
        password_user = 'sudo passwd ' + username
        create_file = 'sudo mkdir ' + root_dir
        chown_file = 'sudo chown -R ' + username + ':' + username + ' ' + root_dir
        find_user = 'sudo id -u ' + username

        sin, sout, err = client.exec_command(find_user, timeout=60)
        sin.write(self.root_password + '\n')
        for i in sout:
            if i:
                return "user exist"

        sin, sout, err = client.exec_command(add_user + ';' + password_user, timeout=60)
        sin.write(self.root_password + '\n' + self.root_password + '\n' + self.root_password + '\n')

        time.sleep(3)
        sin, sout, err = client.exec_command(create_file + ';' + chown_file, timeout=60)
        sin.write(self.root_password + '\n')
        for e in err:
            if e:
                return e

        return "OK"
