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
    prob = self.interestNormalDist.cdf(proposal)
    approved = np.random.uniform() >= (1 - prob)
    if approved:
      self.feedbacks.positive += 1
    else:
      self.feedbacks.negative += 1
    return self

  # TODO: Docs for vote
  def vote(self, candidates_list: list):
    similarity_list = map(lambda candidate:
      self.interestNormalDist.overlap(candidate.interestNormalDist)
    , candidates_list)
    return similarity_list.index(max(similarity_list))

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

class State():
  election_history: list
  citizens: list
  candidates: list
  year: int
  repersentative: Representative

  def election(self):
    votes = map(lambda citizen: citizen.vote(self.candidates), self.citizens)
    vote_count = [0  for i in range(5)]
    for vote in votes:
      vote_count[vote] += 1
    
    result = vote_count.index(max(vote_count))
    self.repersentative = Representative(self.candidates[result])
    election_stats = {
      year: self.year,
      votes: vote_count,
      candidates: self.candidates,
      representative: self.repersentative
    }
    self.election_history.append(election_stats)
    return election_stats

  # returns a list of candidates
  def choice_of_candidates(self):
    candidates: list = []
    citizens = self.citizens
    for i in range(self.candidates_number):
      candidate = citizens.pop(np.random.randint(0, len(citizens)))
      candidates.append(candidate)
    self.candidates = candidates
    return candidates

  def day_simulation(self):
    # 1 - The Representative releases a proposal
    proposal = self.repersentative.new_proposal()

    # 2 - The proposal is evaluated by the citizens
    map(
      lambda citizen: citizen.get_opinion(proposal)
    , self.citizens)

  def get_population_feedback(self):
    feedbacks: list = []
    for citizen in self.citizens:
      feedbacks.append(citizen.feedbacks)
    return feedbacks

  def mandate(self, time: int):
    self.choice_of_candidates()
    election_result = self.election()
    for i in range(time):
      self.day_simulation()
    pfb = self.get_population_feedback()
    return {
      election: election_result,
      population_feedback: pfb
    }

  def __init__(self, population_number, candidates_number):
    self.year = 0
    self.election_history = []
    self.citizens = [Citizen() for i in range(population_number)]
    self.candidates = []
    self.candidates_number = candidates_number
    self.repersentative = None

if __name__ == "__main__":
  state = State(200, 5);
  mandate_time = 1460 # 4 years
  simulation_time = 100000
  for i in range(simulation_time):
    active_mandate_time = 0
    for i in range(active_mandate_time)
