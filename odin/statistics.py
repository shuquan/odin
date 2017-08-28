import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from odin.common import utils

project_name = 'biz_req'

dp = utils.get_dataframe_by_project_name(project_name)
redmine = utils.redmine_connect()
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
# issues[0].custom_fields.get(42).value

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
