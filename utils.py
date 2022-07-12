import streamlit as st
from habanero import Crossref
import numpy as np
import random
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
  titles = []
  for a in article_list:
    strings.append(a.title.lower())
    titles.append(a.title.lower())
    if a.abstract != None:
      strings.append(a.abstract.lower())

  corpus = " ".join(strings)
  corpus_titles = " ".join(titles)
  #vec = CountVectorizer()
  #X = vec.fit_transform(strings)

  return corpus, corpus_titles




def generate_poem(search_string, length):
    
  corpus, titles = get_corpus(search_crossref(search_string))
  corpus = corpus.split()
  titles = titles.split()

  title_pairs = make_pairs(titles)
  title_fw = np.random.choice(titles)
  pairs = make_pairs(corpus)
  first_word = np.random.choice(corpus)

  word_dict = {}
  for word_1, word_2 in pairs:
      if word_1 in word_dict.keys():
          word_dict[word_1].append(word_2)
      else:
          word_dict[word_1] = [word_2]

  title_dict = {}
  for t_word_1, t_word_2 in title_pairs:
      if t_word_1 in title_dict.keys():
          title_dict[t_word_1].append(t_word_2)
      else:
          title_dict[t_word_1] = [t_word_2]

  title_chain = [title_fw]

  for i in range(np.random.choice(list(range(2,4)))):
    title_chain.append(np.random.choice(title_dict[title_chain[-1]]))

  chain = [first_word]
  n_words = length

  for i in range(n_words):
      chain.append(np.random.choice(word_dict[chain[-1]]))


  poem = ' '.join(jitter_poem_string(chain))
  title = ' '.join(title_chain)
  return poem, title

from random import random
def jitter_poem_string(chain):
    poem = []
    space = " "
    newline = "\n"
    for i in range(0, len(chain)):
        # whitespace = randint(1, 10)
        # linebreaks = randint(0, 3)
        which_one = random()
        poem.append(chain[i])
        if which_one >= 0.34 and which_one <= 0.66:
            poem.append(space)
        elif which_one >= 0.67:
            poem.append(newline)



    return poem