from __future__ import with_statement
from fabric.api import run, cd, env, sudo, execute
from fabric.context_managers import prefix


env.hosts = ['sentimos.com.br']


def check_if_beanstalk_tubes_are_empty():
    with cd('/home/artur/Como-nos-Sentimos'):
        with prefix('source /home/artur/.virtualenvs/cns/bin/activate'):
            jobs = run('python check_beanstalk_tubes.py')
            return jobs


def git_pull():
    with cd('/home/artur/Como-nos-Sentimos'):
        run('git pull')


def reload_all():
    jobs = check_if_beanstalk_tubes_are_empty()
    if jobs < 10:
        sudo('service memcached restart')
        sudo('supervisorctl restart all')
        sudo('service nginx restart')
        sudo('touch /etc/uwsgi/apps-enabled/cns_website.ini')


def supervisor_status():
    sudo('supervisorctl status')


def atualiza():
    execute(git_pull)
    execute(reload_all)
