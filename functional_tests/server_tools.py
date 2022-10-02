from fabric.api import *
from fabric.context_managers import settings, shell_env


env.host_string = "ubuntu@superlists-1234-staging.xyz"
env.key_filename = "./aws/ListsWebsite.pem"


def _get_manage_dot_py(host):
    return f"~/sites/{host}/virtualenv/bin/python ~/sites/{host}/manage.py"


def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    run(f"{manage_dot_py} flush --noinput")


def _get_server_env_vars(host):
    env_lines = run(f"cat ~/sites/{host}/.env").splitlines()
    return dict(l.split("=") for l in env_lines if l)


def create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    env_vars = _get_server_env_vars(host)
    with shell_env(**env_vars):
        session_key = run(f"{manage_dot_py} create_session {email}")
        return session_key.strip()
