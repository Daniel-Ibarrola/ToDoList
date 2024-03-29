import random
import os
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = "https://github.com/Daniel-Ibarrola/ToDoList.git"


def _get_latest_source():
    """ Downloads the latest source code from GitHub. """

    # Check if the current directory is a git repo
    if exists(".git"):
        run("git fetch")
    else:
        run(f"git clone {REPO_URL} .")
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"git reset --hard {current_commit}")


def _update_virtualenv():
    """ Creates a virtual environment if doesn't exists and installs
        all dependencies in the requirements file.
    """
    if not exists("virtualenv/bin/pip"):
        run(f"python3.7 -m venv virtualenv")
    run("./virtualenv/bin/pip install -r requirements.txt")


def _create_or_update_dotenv():
    """ Creates or updates a .env file. """
    append(".env", "DJANGO_DEBUG_FALSE=y")
    append(".env", f"SITENAME={env.host}")
    current_contents = run("cat .env")

    if "DJANGO_SECRET_KEY" not in current_contents:
        new_secret = "".join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append(".env", f"DJANGO_SECRET_KEY={new_secret}")

    email_password = os.environ["EMAIL_PASSWORD"]
    append(".env", f"EMAIL_PASWORD={email_password}")


def _update_static_files():
    """ Updates static files """
    run("./virtualenv/bin/python manage.py collectstatic --noinput")


def _update_database():
    """ Applies a migration to the database. """
    run("./virtualenv/bin/python manage.py migrate --noinput")


def deploy():
    site_folder = f"/home/{env.user}/sites/{env.host}"
    run(f"mkdir -p {site_folder}")
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()
