"""Fabfile to deploy localized_classified_ads project"""
from __future__ import with_statement
from fabric.api import (cd , lcd, get, run, local, 
                        settings, sudo, env, put, prefix)
from fabric.contrib.files import exists, upload_template
import time
import os

from fabric.contrib import django

django.settings_module('localized_classified_ads.settings')
from django.conf import settings

env.hosts = ['achetersanscom@ssh.alwaysdata.com',]
env.passwords = {'achetersanscom@ssh.alwaysdata.com':'Sam25sn06', }

def test():
    with cd('localized_classified_ads/public/'):
        print 'ouat'
        upload_template('public/django.fcgi', '.', context={'account_name':'account_name', 'virtualenv_name':'virtualenv_name'})
    #upload_template('public/.htaccess', '/home/achetersanscom/localized_classified_ads/public')


def init_local_db():
    local('./create_template_postgis-1.5.sh')
    try:
        local('dropdb %s' % (settings.DATABASES['default']['NAME']))
    except:
        #print 'no previous db'
        pass
    local('createdb -T template_postgis %s' % (settings.DATABASES['default']['NAME']))
    local('python manage.py syncdb')
    local('python manage.py migrate')
    local('python manage.py create_superuser_userprofile')
    local('python manage.py check_permissions')
    #local('python manage.py create_random_userprofiles')
    #local('python manage.py create_random_ads')
    local('python manage.py runserver')
    # must have initial site features for use with django-dynamicsites

def deploy(account_name="achetersanscom", virtualenv_name="achetersanscom", virtualenv=False, requirements=False):
    local('git archive --format=tar master | gzip > localized_classified_ads.tar.gz')
    put('localized_classified_ads.tar.gz', '.')
    run('rm -rf localized_classified_ads')
    run('mkdir localized_classified_ads')
    run('tar -xvzf localized_classified_ads.tar.gz -C localized_classified_ads')
    run('rm localized_classified_ads.tar.gz')
    put('settings.py', 'localized_classified_ads/settings.py')
    run('chmod +x localized_classified_ads/public/django.fcgi')
    if virtualenv:
        #run('rmvirtualenv achetersanscom')
        #run('mkvirtualenv --no-site-packages achetersanscom')
        if requirements:
            run('pip install --upgrade -E %s -r localized_classified_ads/%s' % (virtualenv_name, requirements))
        else:
            run('pip install --upgrade -E %s -r localized_classified_ads/requirements.txt' % (virtualenv_name))
    with cd('localized_classified_ads/public'):
        put('public/.htaccess', '.')
        upload_template('public/django.fcgi', '.', context={'account_name':account_name, 'virtualenv_name':virtualenv_name})
    with cd('localized_classified_ads'):
        with prefix('workon achetersanscom'):
            run('python manage.py syncdb')
            run('python manage.py migrate ads')
            run('python manage.py collectstatic')
            run('python create_prems_and_contenttype.py')
    with cd('localized_classified_ads/public'):
        run('ln -s ../static static')
        run('ln -s ../../media media')
    local('rm localized_classified_ads.tar.gz')

def update(account_name="achetersanscom", virtualenv_name="achetersanscom", virtualenv=False, requirements=False):
    backup_media()
    deploy(account_name, virtualenv_name, virtualenv, requirements)
    update_media()

def backup_media():
    with cd('localized_classified_ads'):
        run('cp -R media ..')

def update_media():
    with cd('localized_classified_ads'):
        run('rm -rf media')
        run('mv ../media .')
        run('rm public/media')
        with cd('public'):
            run('ln -s ../media media')


def generate_data():
    with cd('localized_classified_ads'):
        run('workon achetersanscom && python manage.py create_superuser_userprofile')
        run('workon achetersanscom && python manage.py check_permissions')
        run('workon achetersanscom && python manage.py create_random_userprofiles')
        run('workon achetersanscom && python manage.py create_random_ads')