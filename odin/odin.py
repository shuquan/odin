# -*- coding: utf-8 -*-
import jieba
import os
import pandas as pd
import pyLDAvis
import pyLDAvis.sklearn
from redminelib import Redmine
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

environ_value = dict(os.environ)

redmine_url = environ_value['REDMINE_URL']
redmine_username = environ_value['REDMINE_USERNAME']
redmine_password = environ_value['REDMINE_PASSWORD']
project_name = 'biz_req'
redmine = Redmine(redmine_url, username=redmine_username,
                  password=redmine_password)
project = redmine.project.get(project_name)
data = []

def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

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
dp["content_cutted"] = dp.description.apply(chinese_word_cut)

tf_vectorizer = CountVectorizer(strip_accents = 'unicode',
                            max_features=100,
                            stop_words='english',
                            max_df = 0.5,
                            min_df = 10)
tf = tf_vectorizer.fit_transform(dp.content_cutted)

lda = LatentDirichletAllocation(n_topics=5, max_iter=50,
                            learning_method='online',
                            learning_offset=50.,
                            random_state=0)

lda.fit(tf)

n_top_words = 20
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)

prepare = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
pyLDAvis.display(prepare)
