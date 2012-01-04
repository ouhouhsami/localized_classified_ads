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

def init_local_db():
    local('./create_template_postgis-1.5.sh')
    try:
        local('dropdb %s' % (settings.DATABASES['default']['NAME']))
    except:
        print 'no previous db'
    local('createdb -T template_postgis %s' % (settings.DATABASES['default']['NAME']))
    local('python manage.py syncdb')
    local('python manage.py migrate')
    local('python manage.py create_superuser_userprofile')
    local('python manage.py check_permissions')
    #local('python manage.py create_random_userprofiles')
    #local('python manage.py create_random_ads')
    local('python manage.py runserver')
    # must have initial site features for use with django-dynamicsites

def deploy(virtualenv=False):
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
        run('pip install --upgrade -E achetersanscom -r localized_classified_ads/requirements.txt')
    with cd('localized_classified_ads'):
        run('workon achetersanscom && python manage.py syncdb')
        run('workon achetersanscom && python manage.py migrate ads')
        run('workon achetersanscom && python manage.py collectstatic')
        run('workon achetersanscom && python create_prems_and_contenttype.py')
    with cd('localized_classified_ads/public'):
        run('ln -s ../static static')
        run('ln -s ../../media media')
    local('rm localized_classified_ads.tar.gz')

def update():
    backup_media()
    deploy()
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