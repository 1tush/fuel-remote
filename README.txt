This package allow to run fuel qa tests on remote server without manual login to it

=== INSTALLATION ==

pip install git+https://github.com/1tush/fuel-remote.git

=== USAGE ===

rem [-h] [--host REMOTE_HOST] [--path REMOTE_PATH] [--venv VENV_PATH]
           [--iso-path ISO_PATH] [--ipython] [--screen]
           {init,sync,execute,test,shell} ...

Helper to run fuel-qa tests remotely

optional arguments:
  -h, --help            show this help message and exit
  --host REMOTE_HOST    Remote host
  --path REMOTE_PATH    Remote path
  --venv VENV_PATH      Remote virtualenv path
  --iso-path ISO_PATH   ISO path
  --ipython, -i         Use ipython to run tests
  --screen, -s          Run commands inside screen

Actions:
  {init,sync,execute,test,shell}
    init                Make local config template
    sync                Sync local catalog with remote
    execute             Execute command on remote server
    test                Run test group on remote server
    shell               Run bash on remote server

