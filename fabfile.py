# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import run, cd, env, sudo, execute
from fabric.context_managers import prefix


env.hosts = ['ubuntu@sentimos.com.br']


def check_if_beanstalk_tubes_are_empty():
    with cd('/home/ubuntu/Como-nos-Sentimos'):
        jobs = run('python check_beanstalk_tubes.py')
        return jobs


def git_pull():
    with cd('/home/ubuntu/Como-nos-Sentimos'):
        run('git pull')


def reload_all():
    jobs = check_if_beanstalk_tubes_are_empty()
    if int(jobs) < 10:
        sudo('service memcached restart')
        sudo('supervisorctl restart all')
        sudo('service nginx restart')
        sudo('touch /etc/uwsgi/apps-enabled/cns_website.ini')


def supervisor_status():
    sudo('supervisorctl status')


def atualiza():
    execute(git_pull)
    execute(reload_all)
