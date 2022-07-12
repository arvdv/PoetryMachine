import streamlit as st
from habanero import Crossref
import numpy as np

cr = Crossref()

class Article:
  def __init__(self, _authors, _title, _date, _abstract=None):
    self.authors = _authors
    self.title = _title
    self.date = _date
    self.abstract = _abstract


def parse_authors(crossref_return):
  try:
    author_list = crossref_return['author']
    authors = []
    for a in author_list:
      authors.append(f"{a['given']}, {a['family']}")
  except:
    authors = None

  return authors

def parse_abstract(crossref_return):

    try:
        abstract = crossref_return['abstract']
    except:
        abstract = None

    return abstract

def parse_date(crossref_return):
    return crossref_return['created']['date-time']

def search_crossref(query):

  works = cr.works(query=query)['message']['items']
  
  articles = []

  for w in works:
    authors = parse_authors(w)
    title = w['title'][0]
    abstract = parse_abstract(w)
    date = parse_date(w)

    articles.append(Article(authors, title, date, abstract))


  return articles

def make_pairs(corpus):
    for i in range(len(corpus)-1):
        yield (corpus[i], corpus[i+1])
        
def get_corpus(article_list):
  strings = []
  for a in article_list:
    strings.append(a.title.lower())
    if a.abstract != None:
      strings.append(a.abstract.lower())

  corpus = " ".join(strings)
  #vec = CountVectorizer()
  #X = vec.fit_transform(strings)

  return corpus


def generate_poem(search_string, length):
    
  corpus = get_corpus(search_crossref(search_string)).split()
  corpus = corpus
  pairs = make_pairs(corpus)
  first_word = np.random.choice(corpus)

  word_dict = {}
  for word_1, word_2 in pairs:
      if word_1 in word_dict.keys():
          word_dict[word_1].append(word_2)
      else:
          word_dict[word_1] = [word_2]


  chain = [first_word]
  n_words = length

  for i in range(n_words):
      chain.append(np.random.choice(word_dict[chain[-1]]))


  poem = ' '.join(chain)
  return poem