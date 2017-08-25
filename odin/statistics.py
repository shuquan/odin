%matplotlib inline
# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import os
import pandas as pd
from redminelib import Redmine

environ_value = dict(os.environ)

# Validate the REDMINE_* before
redmine_url = environ_value['REDMINE_URL']
redmine_username = environ_value['REDMINE_USERNAME']
redmine_password = environ_value['REDMINE_PASSWORD']
project_name = 'biz_req'
redmine = Redmine(redmine_url, username=redmine_username,
                  password=redmine_password)
issues = redmine.issue.filter(status_id='*', project_id=project_name)
data = []

for i in issues:
    data.append([
#         i.attachments,
         i.author.name,
#         i.changesets,
#         i.children,
         i.created_on.strftime('%Y-%m-%d'),
#         i.custom_fields,
         i.description,
#         i.done_ratio,
         i.id,
#         i.journals,
         i.priority.name,
         i.project.name,
#         i.relations,
#         i.start_date,
         i.status.name,
         i.subject,
#         i.time_entries,
         i.tracker.name,
         i.updated_on.strftime('%Y-%m-%d'),
#         i.watchers
     ])

dp = pd.DataFrame(data,
                  columns=['author', 'created_on', 'description', 'id',
                           'priority', 'project', 'status', 'subject',
                           'tracker', 'updated_on'])
# Status by datetime

dp = dp[dp.tracker == u'错误']
d = {}
for i in redmine.issue_status.all():
    dp_tmp = dp[dp.status == i.name].groupby('created_on').size()
    dp_tmp.index = pd.to_datetime(dp_tmp.index)
    d[i.name] = dp_tmp

total = pd.DataFrame(d)
total['2017-8-18':'2017-8-26'].plot.bar(stacked=True)
