import numpy as np
import scipy.stats as spt
import itertools
from statistics import NormalDist
from typing import List, Dict, NewType

'''
  Citizen - every actor of our system is a citizen.
  attributes: {
    interestLevels,
    feedbacks: {
      positive,
      negative
    }
  }
'''
# TODO: typing
class Citizen:
  id_iter = itertools.count()

  # TODO: Docs for get_opinion
  def get_opinion(self, proposal):
    return self.interestNormalDist.cdf(proposal)
    pass

  # TODO: Docs for vote
  def vote(self, candidates_list: list):
    similarity_list = map(lambda candidate:
      self.interestNormalDist.overlap(candidate.interestNormalDist)
    , candidates_list)
    return similarity_list.index(max(similarity_list))
    pass



  def __init__(self):
    self.id = next(Citizen.id_iter)
    self.mean = np.random.randint(-100, 100)
    self.stddev = 1
    self.feedbacks = {
      positive: 0,
      negative: 0
    }
    self.interestNormalDist = NormalDist(mu = self.mean, sigma = self.stddev)

class Representative(Citizen):
  # TODO: docs for new_proposal
  def new_proposal(self):
    return self.interestNormalDist.samples(1)
    pass


class State():
  election_history: list
  citizens: list
  candidates: list
  year: int

  def election(self):
    votes = map(lambda citizen: citizen.vote(self.candidates), self.citizens)
    vote_count = [0  for i in range(5)]
    for vote in votes:
      vote_count[vote] += 1
    
    result = vote_count.index(max(vote_count))
    self.repersentative = self.candidates[result]
    election_stats = {
      year: self.year,
      votes: vote_count,
      candidates: self.candidates,
      representative: self.repersentative
    }
    self.election_history.append(election_stats)
    return election_stats
    pass

  # returns a list of candidates
  def choice_of_candidates(self):
    candidates: list = []
    citizens = self.citizens
    for i in range(self.candidates_number):
      candidate = citizens.pop(np.random.randint(0, len(citizens)))
      candidates.append(candidate)
    self.candidates = candidates
    return candidates
    pass

  def day_simulation(self):

    pass

  def __init__(self, population_number, candidates_number):
    self.year = 0
    self.election_history = []
    self.citizens = [Citizen() for i in range(population_number)]
    self.candidates = []
    self.candidates_number = candidates_number
    self.repersentative = None
  pass


print(x)