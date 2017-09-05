# -*- coding: utf-8 -*-
"""Utilities and helper functions."""

import os
import pandas as pd
from redminelib import Redmine

environ_value = dict(os.environ)

# Validate the REDMINE_* before
redmine_url = environ_value['REDMINE_URL']
redmine_username = environ_value['REDMINE_USERNAME']
redmine_password = environ_value['REDMINE_PASSWORD']

def redmine_connect(redmine_url = environ_value['REDMINE_URL'],
                    redmine_username = environ_value['REDMINE_USERNAME'],
                    redmine_password = environ_value['REDMINE_PASSWORD']):
    redmine = Redmine(redmine_url, username=redmine_username,
                      password=redmine_password)
    return redmine

def get_custom_field_id_by_name(custom_field_name):
    redmine = redmine_connect()
    custom_field_set = {}
    for i in redmine.custom_field.all():
        custom_field_set[i.name] = i.id

    return custom_field_set[custom_field_name]

def get_dataframe_by_project_name(project_name):
    redmine = redmine_connect()
    issues = redmine.issue.filter(status_id='*', project_id=project_name)
    data = []
    custom_field_feature_id = get_custom_field_id_by_name(u'功能模块')
    custom_field_version_id = get_custom_field_id_by_name(u'版本信息')

    for i in issues:
        l = [
    #         i.attachments.total_count,
             i.author.name,
    #         i.changesets,
    #         i.children,
             i.created_on.strftime('%Y-%m-%d'),
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
         ]
        if hasattr(i,'custom_fields') and i.custom_fields.get(custom_field_feature_id) is not None:
            l.append(i.custom_fields.get(custom_field_feature_id).value)
        else:
            l.append('')
        if hasattr(i,'custom_fields') and i.custom_fields.get(custom_field_version_id) is not None:
            l.append(i.custom_fields.get(custom_field_version_id).value)
        else:
            l.append('')
        data.append(l)

    dp = pd.DataFrame(data,
                      columns=['author', 'created_on',
                               'description', 'id',
                               'priority', 'project', 'status', 'subject',
                               'tracker', 'updated_on', 'module','version'])

    dp.created_on = pd.to_datetime(dp.created_on)
    dp.updated_on = pd.to_datetime(dp.updated_on)
    return dp
