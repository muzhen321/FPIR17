
import string


def get_words(file_path):
    """Return a list of words from a file, converted to lower case."""
    with open(file_path, encoding='utf-8') as hfile:
        return hfile.read().lower().split()


def get_needwords(words, stopwords):

    """去stopwords"""
    k = list(filter(lambda x: x not in stopwords, words))
    """转小写"""
    lower_words = []
    for i in k:
        lower_words.append(i.lower())
    words_new = []
    """去标点 python3  translate()参数只能是一个dict 对应数字"""
    remove_punct_map = dict.fromkeys(map(ord, string.punctuation))
    for i in lower_words:
        words_new.append(i.translate(remove_punct_map))
    return words_new


"""create index  Model"""
"""title/path/content就是所谓的字段。每个字段对应索引查找目标文件的一部分信息，例子就是建立索引的模式：索引内容包括title/path/content。一个字段建立了索引，意味着它能够被搜索；也能够被存储，意味着返回结果"""
from whoosh.index import create_in
from whoosh.fields import *
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)


"""create the store direction of index"""
"""Make sure you have the directory "index" created beforehand in the folder where you start the notebook"""
import os.path
from whoosh.index import open_dir
from whoosh.index import create_in


if not os.path.exists("index"):   #如果目录index不存在则创建
    os.mkdir("index")
ix = create_in("index", schema)   #按照schema模式创建索引目录

ix = open_dir("index")            #打开该目录一遍存储索引文件


"""write index  写入索引内容"""
writer = ix.writer()

writer.add_document(title=u"First document", path=u"/a", content=u"The beauty of me is that I'm very rich.")
writer.add_document(title=u"Second document", path=u"/b", content=u"I loved my previous life. I had so many things going.")
writer.add_document(title=u"third document", path=u"/c", content=u"This is more work than in my previous life.")
writer.add_document(title=u"fourth document", path=u"/d", content=u"I've said if Ivanka weren't my daughter, perhaps I'd be dating her.")
writer.add_document(title=u"fifth document", path=u"/e", content=u"I have never seen a thin person drinking Diet Coke.")

writer.commit()


"""Querz 搜索"""

from whoosh.qparser import QueryParser
from whoosh.query import *
myquery = And([Term("content", u"previous "), Term("content", "life")])

with ix.searcher() as searcher:
    parser = QueryParser("content", ix.schema)
    myquery = parser.parse("previous")
    results = searcher.search(myquery)
    print(results[0], results[0].score)


"""ranking functions"""

from whoosh import scoring

w = scoring.TF_IDF()
with ix.searcher(weighting=w) as searcher:
    query = QueryParser("content", ix.schema).parse("previous AND life")
    results = searcher.search(query)
    print(results[0], results[0].score)


with ix.searcher(weighting=w) as searcher:
    query2 = QueryParser("content", ix.schema).parse("life AND NOT work")
    results2 = searcher.search(query)
    print(results2[0], results2[0].score)

