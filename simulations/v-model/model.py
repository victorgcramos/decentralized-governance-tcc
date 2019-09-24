import numpy as np
import itertools
import json
from statistics import NormalDist
from typing import List, Dict, NewType
import time as timepackage
import helpers as hp

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
    self.stddev = np.random.randint(1, 10)
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
  day: int
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
      "day": self.day,
      "votes": vote_count,
      "candidates": dict_candidates,
      "representative": {
        "id": self.repersentative.id,
        "mean": self.repersentative.mean,
        "stddev": self.repersentative.stddev
      }
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
    # Increment day counter
    self.day += 1

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

  # TODO: parallelize this procedure
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
    # hp.print_progress_bar(0, time, prefix = 'Simulation Progress:', suffix = 'Complete', length = 50)
    for i in range(time):
      self.day_simulation()
      # timepackage.sleep(0.0002)
      # hp.print_progress_bar(i + 1, time, prefix = 'Simulation Progress:', suffix = 'Complete', length = 50)

    accpfb = self.get_accumulated_population_feedback()
    self.reset_population_feedback()
    return {
      "election": election_result,
      "population_feedback": accpfb
    }

  def __init__(self, population_number, candidates_number):
    self.day = 0
    self.election_history = []
    self.citizens = [Citizen() for i in range(population_number)]
    self.candidates = []
    self.candidates_number = candidates_number
    self.repersentative = None
    self.accumulated_feedback_log = []
    self.proposal_log = []

if __name__ == "__main__":
  population_number: int = 60
  candidates_number: int = 5
  term_of_office_time: int = 365 * 4
  terms_of_office: int = 100
  terms_of_office_history: list = []
  acc_fb_coordinates = {
    "positives": [],
    "negatives": []
  }

  state: State = State(population_number, candidates_number)
  hp.print_progress_bar(0, terms_of_office, prefix = 'Simulation Progress:', suffix = 'Complete', length = 50)
  for i in range(terms_of_office):
    print("\n\nTerm of office", i+1)
    term_of_office_status = state.term_of_office(term_of_office_time)
    terms_of_office_history.append(term_of_office_status)
    timepackage.sleep(0.0002)
    hp.print_progress_bar(i+1, terms_of_office, prefix = 'Simulation Progress:', suffix = 'Complete', length = 50)
  
  acc_fb_coordinates["positives"] += list(
    map(lambda record: record["population_feedback"]["positives"], terms_of_office_history))
  acc_fb_coordinates["negatives"] += list(
    map(lambda record: record["population_feedback"]["negatives"], terms_of_office_history))
  
  time = list(range(terms_of_office))
  
  hp.save_records(time,
    acc_fb_coordinates["positives"],
    acc_fb_coordinates["negatives"],
    terms_of_office_history)
  

