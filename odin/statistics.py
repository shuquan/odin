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
    if hasattr(i,'custom_fields') and i.custom_fields.get(42) is not None:
        l.append(i.custom_fields.get(42).value)
    else:
        l.append('')
    if hasattr(i,'custom_fields') and i.custom_fields.get(24) is not None:
        l.append(i.custom_fields.get(24).value)
    else:
        l.append('')
    data.append(l)

dp = pd.DataFrame(data,
                  columns=['author', 'created_on',
                           'description', 'id',
                           'priority', 'project', 'status', 'subject',
                           'tracker', 'updated_on', 'module','version'])

# Status by datetime

dp = dp[dp.tracker == u'错误']
d = {}
for i in redmine.issue_status.all():
    dp_tmp = dp[dp.status == i.name].groupby('created_on').size()
    dp_tmp.index = pd.to_datetime(dp_tmp.index)
    d[i.name] = dp_tmp

total = pd.DataFrame(d)
total['2017-8-18':'2017-8-26'].plot.bar(stacked=True)

# Status by custom_field

# Get value
issues[0].custom_fields.get(42).value

# Get all possible_values of custom_field

for i in redmine.custom_field.all().get(42)['possible_values']:
    print i['value']

for i in redmine.custom_field.all():
    print i.id, i

# 1 Scrum周期（已弃用，用于追踪过去数据）
# 2 剩余小时
# 3 价值
# 6 风险
# 7 发生几率
# 8 错误描述
# 10 QA负责人
# 12 提问者
# 14 错误类型
# 22 关键字
# 24 版本信息
# 28 Testcase
# 30 问题阶段
# 32 项目开始日期
# 34 实施开始日期
# 36 项目售后截止日期
# 38 项目阶段
# 40 预期修复
# 42 功能模块
# 48 社区Bug地址链接

# 功能模块
dp = dp[dp.tracker == u'错误']
d = {}
for i in redmine.custom_field.all().get(42)['possible_values']:
    dp_tmp = dp[dp.module == i['value']].groupby('status').size()
    d[i['value']] = dp_tmp
total = pd.DataFrame(d)
total.T.plot.bar(stacked=True)

# 版本信息
dp = dp[dp.tracker == u'错误']
d = {}
for i in redmine.custom_field.all().get(24)['possible_values']:
    dp_tmp = dp[dp.version == i['value']].groupby('status').size()
    d[i['value']] = dp_tmp
total = pd.DataFrame(d)
total.T.plot.bar(stacked=True)
