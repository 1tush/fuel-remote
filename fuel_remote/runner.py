# -*- coding: utf-8 -*-

import sys
import subprocess

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)


class Runner(object):

    def __init__(self, remote_host, remote_path, venv_path, iso_path,
                 envs, ipython=True, screen=False, **kwargs):
        self.remote_host = remote_host
        self.remote_path = '${HOME}/%s' % remote_path
        self.iso_path = '${HOME}/%s' % iso_path
        self.venv_path = '${HOME}/%s' % venv_path
        self.envs = envs
        self.ipython = ipython
        self.screen = screen
        if self.ipython:
            self.python_executable = '{}/bin/ipython'.format(self.venv_path)
        else:
            self.python_executable = '{}/bin/python'.format(self.venv_path)
        self.envs.update({
            'ISO_PATH': self.iso_path,
            'VENV_PATH': self.venv_path,
            'PYTHONPATH': '${PYTHONPATH:+${PYTHONPATH}:}'
                          '%s' % self.remote_path,
            'LOGS_DIR': '{}/logs'.format(self.remote_path)
        })

    def prepare_command(self, command):
        if command.startswith('python ') or command == 'python':
            script, args = command.lstrip('python').strip().split(' ', 1)
            if self.ipython:
                args = " -- {}".format(args)
            command = '{} {} {}'.format(self.python_executable, script, args)
        return command

    def sync(self):
        logger.debug('Run sync')
        excludes = [
            r'\.git*',
            r'logs/*',
            r'*.pyc',
            r'ca.*',
            r'\.tox*',
            r'*__pycache__*',
            r'\.cache*',
            r'doc/_build*',
        ]
        command = ['rsync']
        command += ["--exclude={}".format(x) for x in excludes]
        command += ['-avz', '.',
                    '{0.remote_host}:{0.remote_path}'.format(self)]
        subprocess.call(command)

    def execute(self, command):
        if isinstance(command, (basestring)):
            command = [command]
        command = ' '.join(command)
        command_list = ['export %s' % ' '.join('%s=%s' % (k, v)
                        for k, v in self.envs.items())]
        command_list += ['cd {}'.format(self.remote_path)]
        command_list += [self.prepare_command(command)]
        if self.screen:
            command_list[-1:] = ['rm screenlog.0',
                                 'screen -L ' + command_list[-1]]
        command = "; ".join(x.replace(r"'", r"\'")
                            for x in command_list)
        command = "ssh -t {} '{}'".format(self.remote_host, command)
        logger.debug('Running command: \n{}'.format(command))
        subprocess.call(command,
                        stdin=sys.stdin,
                        stdout=sys.stdout,
                        stderr=sys.stderr,
                        shell=True)

    def shell(self):
        self.sync()
        self.execute('bash --init-file '
                     '{0.venv_path}/bin/activate'.format(self))

    def test(self, groups):
        self.sync()
        groups_string = ' '.join('--group={}'.format(x) for x in groups)
        self.execute('python fuelweb_test/run_tests.py -q --nologcapture '
                     '--with-xunit {}'.format(groups_string))
