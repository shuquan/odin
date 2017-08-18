# -*- coding: utf-8 -*-
import os
from redminelib import Redmine

environ_value = dict(os.environ)

redmine_url = environ_value['REDMINE_URL']
redmine_username = environ_value['REDMINE_USERNAME']
redmine_password = environ_value['REDMINE_PASSWORD']
project_name = 'biz_req'
redmine = Redmine(redmine_url, username=redmine_username, password=redmine_password)
project = redmine.project.get(project_name)
print project.issues[0].subject.encode('utf-8')
