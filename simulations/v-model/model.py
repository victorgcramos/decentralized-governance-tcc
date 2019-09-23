import numpy as np
import itertools
import json
from statistics import NormalDist
from typing import List, Dict, NewType
import matplotlib.pyplot as plt
from datetime import datetime

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
    prob = self.interest_curve.cdf(proposal)
    approved = np.random.uniform() >= (1 - prob)
    if approved:
      self.feedbacks["positive"] += 1
      self.feedback_log.append(1)
    else:
      self.feedbacks["negative"] += 1
      self.feedback_log.append(0)
    return self

  # TODO: Docs for vote
  def vote(self, candidates_list: list):
    similarity_list = list(map(lambda candidate:
      self.interest_curve.overlap(candidate.interest_curve)
    , candidates_list))
    sim = similarity_list.index(max(similarity_list))
    return sim

  def __init__(self):
    self.id = next(Citizen.id_iter)
    self.mean = np.random.randint(-100, 100)
    self.stddev = 5
    self.feedbacks = {
      "positive": 0,
      "negative": 0
    }
    self.interest_curve = NormalDist(mu = self.mean, sigma = self.stddev)
    self.feedback_log = []

class Representative(Citizen):
  # TODO: docs for new_proposal
  def new_proposal(self):
    return self.interest_curve.samples(1).pop()
  
  def __init__(self, citizen: Citizen):
    self.id = citizen.id
    self.mean = citizen.mean
    self.stddev = citizen.stddev
    self.feedbacks = citizen.feedbacks
    self.interest_curve = citizen.interest_curve


class State():
  election_history: list
  citizens: list
  candidates: list
  year: int
  repersentative: Representative

  def election(self):
    votes = list(map(lambda citizen: citizen.vote(self.candidates), self.citizens))
    vote_count = [0  for i in range(self.candidates_number)]
    for vote in votes:
      vote_count[vote] += 1
    
    dict_candidates = list(map(lambda candidate:
    {
      "id": candidate.id,
      "mean": candidate.mean,
      "stddev": candidate.stddev
    },
    self.candidates))
    result = vote_count.index(max(vote_count))
    self.repersentative = Representative(self.candidates[result])
    election_stats = {
      "year": self.year,
      "votes": vote_count,
      "candidates": json.dumps(dict_candidates),
      "representative": json.dumps({
        "id": self.repersentative.id,
        "mean": self.repersentative.mean,
        "stddev": self.repersentative.stddev
      })
    }
    self.election_history.append(election_stats)
    return election_stats

  # returns a list of candidates
  def choice_of_candidates(self):
    candidates: list = []
    citizens = self.citizens
    for i in range(self.candidates_number):
      candidate = citizens[np.random.randint(0, len(citizens))]
      candidates.append(candidate)
    self.candidates = candidates
    return candidates

  def day_simulation(self):
    # 1 - The Representative releases a proposal
    proposal = self.repersentative.new_proposal()
    self.proposal_log.append(proposal)

    # 2 - The proposal is evaluated by the citizens
    list(map(
      lambda citizen: citizen.get_opinion(proposal)
    , self.citizens))

  def get_population_feedback(self):
    feedbacks: list = []
    for citizen in self.citizens:
      feedbacks.append(citizen.feedbacks)
    return feedbacks
  
  def get_accumulated_population_feedback(self):
    fbs = self.get_population_feedback()
    acc_fbs = {
      "positives": 0,
      "negatives": 0
    }
    for fb in fbs:
      acc_fbs["positives"] += fb["positive"]
      acc_fbs["negatives"] += fb["negative"]
    
    return acc_fbs

  def get_accumulated_feedback_log(self):
    citizen_props = self.citizens[0]
    acc_fb_log = []
    acc_fb_default = {
      "positive": 0,
      "negative": 0
    }
    for i in range(len(citizen_props.feedback_log)):
      acc_fb = acc_fb_default.copy()
      for citizen in self.citizens:
        if citizen.feedback_log[i] == 0:
          acc_fb["negative"] += 1
        else:
          acc_fb["positive"] += 1
      acc_fb_log.append(acc_fb)
    self.accumulated_feedback_log = acc_fb_log
    return acc_fb_log

  def reset_population_feedback(self):
    for citizen in self.citizens:
      citizen.feedbacks = {
        "positive": 0,
        "negative": 0
      }

  def term_of_office(self, time: int):
    self.choice_of_candidates()
    election_result = self.election()
    for i in range(time):
      self.day_simulation()
    accpfb = self.get_accumulated_population_feedback()
    self.reset_population_feedback()
    return {
      "election": election_result,
      "population_feedback": accpfb
    }

  def __init__(self, population_number, candidates_number):
    self.year = 0
    self.election_history = []
    self.citizens = [Citizen() for i in range(population_number)]
    self.candidates = []
    self.candidates_number = candidates_number
    self.repersentative = None
    self.accumulated_feedback_log = []
    self.proposal_log = []

if __name__ == "__main__":
  population_number: int = 600
  candidates_number: int = 5
  term_of_office_time: int = 365 # 4 years
  terms_of_office: int = 20
  terms_of_office_history: list = []
  acc_fb_log_coordinates = {
    "positives": [],
    "negatives": []
  }

  state: State = State(population_number, candidates_number)
  
  for i in range(terms_of_office):
    term_of_office_status = state.term_of_office(term_of_office_time)
    terms_of_office_history.append(term_of_office_status)
    acc_fb_log = state.get_accumulated_feedback_log()
  
  acc_fb_log_coordinates["positives"] += list(
    map(lambda acc_fb: acc_fb["positive"], acc_fb_log))
  time = list(range(term_of_office_time * terms_of_office))
  plt.plot(time, acc_fb_log_coordinates["positives"])
  plt.savefig("images/temp/%s.png"% datetime.now().isoformat())

  # print(terms_of_office_history)

