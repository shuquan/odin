# -*- coding: utf-8 -*-
import os
import pandas as pd
from redminelib import Redmine

environ_value = dict(os.environ)

redmine_url = environ_value['REDMINE_URL']
redmine_username = environ_value['REDMINE_USERNAME']
redmine_password = environ_value['REDMINE_PASSWORD']
project_name = 'biz_req'
redmine = Redmine(redmine_url, username=redmine_username,
                  password=redmine_password)
project = redmine.project.get(project_name)
data = []

for i in project.issues:
    data.append([
#         i.attachments,
         i.author.name,
#         i.changesets,
#         i.children,
         i.created_on.isoformat(),
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
         i.updated_on.isoformat(),
#         i.watchers
     ])

dp = pd.DataFrame(data,
                  columns=['author', 'created time', 'description', 'id',
                           'priority', 'project', 'status', 'subject',
                           'tracker', 'updated time'])
