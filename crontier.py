#!/usr/bin/env python3.8
# coding: utf-8

from os import path, mknod
from re import search
from app.setting import CRON_FILE
from app.module.logger_module import ShieldLogger

mylogger = ShieldLogger('crontier_module')


def validate_time_cron(timerun: str) -> bool:
    regex = r'(@(annually|yearly|monthly|weekly|daily|hourly|reboot))|(@every (\d+(ns|us|µs|ms|s|m|h))+)|((((\d+,)+\d+|(\d+(\/|-)\d+)|\d+|\*) ?){5,7})'
    if search(regex, timerun):
        return True
    return False

def init():
    # create cron file
    if not path.isfile(CRON_FILE):
        mknod(CRON_FILE)

def AddCron(timerun: str, command: str) -> bool:
    # check it exist or no
    with open(CRON_FILE, 'r') as file:
        for line in file.readlines():
            if timerun in line and command in line:
                mylogger.log_warning(f'cron exist in {CRON_FILE}')
                return False
    # add cron
    with open(CRON_FILE, 'a') as file:
        file.write(f'{timerun} {command}')
        mylogger.log_info(f'cron "{timerun} {command}" added in {CRON_FILE}')
    return True

def DeleteCron(timerun: str, command: str) -> bool:
    with open(CRON_FILE, 'r') as file:
        lines = file.readlines()

    # cron for track
    cron_deleted = False

    with open(CRON_FILE, 'w') as file:
        for line in lines:
            if timerun in line and command in line:
                cron_deleted = True
                continue
            file.write(line)

    # Log if cron was deleted or not
    if cron_deleted:
        mylogger.log_info(f'Cron "{timerun} {command}" deleted from {CRON_FILE}')
    else:
        mylogger.log_warning(f'Cron "{timerun} {command}" not found in {CRON_FILE}')

    return cron_deleted




# init()

# AddCron('* * * * *' , 'python3 test')

# AddCron('* * * * *' , 'python3 test')

# AddCron('3 * * * *' , 'python3 test')

# AddCron('3 * * * *' , 'python3 test1')
