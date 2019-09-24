# Print iterations progress
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime as dt
import json

def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
  """
  Call in a loop to create terminal progress bar
  @params:
      iteration   - Required  : current iteration (Int)
      total       - Required  : total iterations (Int)
      prefix      - Optional  : prefix string (Str)
      suffix      - Optional  : suffix string (Str)
      decimals    - Optional  : positive number of decimals in percent complete (Int)
      length      - Optional  : character length of bar (Int)
      fill        - Optional  : bar fill character (Str)
  """
  percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
  filledLength = int(length * iteration // total)
  bar = fill * filledLength + '-' * (length - filledLength)
  print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
  # Print New Line on Complete
  if iteration == total: 
      print()

def save_records(chart_x: list, chart_y1: list, chart_y2: list, history: list):
  folder_name = "results/temp/%s" % dt.now().isoformat()
  Path(folder_name).mkdir(exist_ok=True) 
  # Chart creation
  plt.plot(chart_x, chart_y1)
  plt.plot(chart_x, chart_y2)
  figpath = folder_name + "/positive_feedback_chart.png"
  plt.savefig(figpath)
  
  # JSON File saving
  with open("%s/history.json"% folder_name, 'w') as outfile:
    json.dump(history, outfile)

  print("\n\nJOB DONE! Check the output folders for results:\n",
    "- JSON OUTPUT for TOO history: %s/history.json\n"% folder_name,
    "- Chart for simulation: %s/positive_feedback_chart.png\n\n"% folder_name)