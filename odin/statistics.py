# -*- coding: utf-8 -*-
"""
研发绩效度量指标体系的指标分成四组[1]：

1. 响应力，反映研发组织响应市场要求的能力，包括需求耗费时长，时长分布图K值两个指标；
2. 质量，反映研发组织交付质量，包括生产缺陷需求比，测试缺陷需求比两个指标；
3. 可用度，反映研发组织管理的系统或服务的稳定性，包括系统可用度或服务可用度指标；
4. 效能，反映研发组织的交付效率，包括需求吞吐率，流动效率两个指标。

1.1 需求耗费时长反映研发组织交付需求的速度。
(1)单一需求耗费时长=需求上线时间-需求提出时间
(2)需求耗费时长=百分位数（所有单一需求耗费时长，85%）
如果研发组织内存在多个不同需求类型，（常规需求、紧急需求和缺陷）那么就需要将这个指标分成几个不同
的指标，如常规需求耗费时长，紧急需求耗费时长以及缺陷修复时长等。
1.2 需求耗费时长分布K值
需求耗费时长分布K值反应需求耗费时长的分布特征。为了计算需求耗费时长分布K值，需要先绘制需求耗费时
长分布图。分布图是一个柱状图，横轴上X位置柱状高度是需求耗费时长为X天的需求的个数。

符合韦伯分布（Weibull Distribution），其一个重要特点就是有一个众数尖峰和一个长尾。众数代表大
多数需求可以在一个时长区间内交付，是研发系统交付常态；而长尾代表交付系统的意外情况。韦伯分布有两
个参数，一个是λ，一个是k。λ决定了众数峰值的高度，k决定了曲线的形状。
如果K值小于1，那么这个研发交付系统是非常脆弱的，不具备可预测性，需求可能很快交付，也可能会非常慢。
如果K值大于2，那么需求交付整体上都很慢，但可预测性比较强；软件开发组织的K值会在1.0到2.0之间。

[1]https://mp.weixin.qq.com/s/XSkUooJdGGxV8u2_N6J_XA
"""
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from odin.common import utils

project_name = 'biz_req'

dp = utils.get_dataframe_by_project_name(project_name)
redmine = utils.redmine_connect()

"""
Initialize basic DataFrame and set
"""

dp_bug = dp[dp.tracker == u'错误']
dp_bug.loc[:,'interval'] = dp_bug.updated_on - dp_bug.created_on
dp_bug_resovled = dp_bug[dp_bug.status == u'已解决']
custom_field_feature_id = utils.get_custom_field_id_by_name(u'功能模块')
custom_field_version_id = utils.get_custom_field_id_by_name(u'版本信息')

"""
X: datetime
Y: # of issue and show the status composition
"""

d = {}
for i in redmine.issue_status.all():
    dp_tmp = dp_bug[dp_bug.status == i.name].groupby('created_on').size()
    d[i.name] = dp_tmp

total = pd.DataFrame(d)
total['2017-8-18':'2017-8-26'].plot.bar(stacked=True)

"""
X: feature
Y: # of issue and show the status composition
"""

d = {}
for i in redmine.custom_field.all().get(custom_field_feature_id)['possible_values']:
    dp_tmp = dp_bug[dp_bug.module == i['value']].groupby('status').size()
    d[i['value']] = dp_tmp
total = pd.DataFrame(d)
total.T.plot.bar(stacked=True)

"""
X: version
Y: # of issue and show the status composition
"""

d = {}
for i in redmine.custom_field.all().get(custom_field_version_id)['possible_values']:
    dp_tmp = dp_bug[dp_bug.version == i['value']].groupby('status').size()
    d[i['value']] = dp_tmp
total = pd.DataFrame(d)
total.T.plot.bar(stacked=True)

"""
耗费时长
"""

dp_bug_resovled.groupby('interval').size().plot()

"""
X: resovled duration
Y: # of issue and show the feature composition
"""

d = {}
for i in redmine.custom_field.all().get(custom_field_feature_id)['possible_values']:
    dp_tmp = dp_bug_resovled[dp_bug_resovled.module == i['value']].groupby('interval').size()
    d[i['value']] = dp_tmp
total = pd.DataFrame(d)
total.plot.bar(stacked=True)

"""
X: resovled duration
Y: # of issue and show the version composition
"""

d = {}
for i in redmine.custom_field.all().get(custom_field_version_id)['possible_values']:
    dp_tmp = dp_bug_resovled[dp_bug_resovled.version == i['value']].groupby('interval').size()
    d[i['value']] = dp_tmp
total = pd.DataFrame(d)
total.plot.bar(stacked=True)

"""
生产缺陷需求比:
生产缺陷需求比反应了研发组织的交付质量。在给定时间内，生产缺陷需求比可以这样计算:
生产缺陷需求比=生产缺陷数量/上线需求规模

使用这个指标的一个挑战是如何确定需求规模。这个首先要看企业是不是已经有一套可行的需求规模估算
体系，如功能点，UCP等等。如果有，就可以延续现有的需求规模估算方式。如果没有，那么我强烈建议，
在需求上游对需求进行适当拆分，保证需求规模相对均匀，然后使用需求个数来反映需求规模。
"""
