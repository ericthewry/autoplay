
"""Text Adventure Registration for T2T."""
import re
import csv

from tensor2tensor.data_generators import problem
from tensor2tensor.data_generators import text_problems
from tensor2tensor.layers import common_hparams
from tensor2tensor.utils import registry

# Use register_model for a new T2TModel
# Use register_problem for a new Problem
# Use register_hparams for a new hyperparameter set


@registry.register_hparams
def my_very_own_hparams():
  # Start with the base set
  hp = common_hparams.basic_params1()
  # # Modify existing hparams
  # hp.num_hidden_layers = 2
  # # Add new hparams
  # hp.add_hparam("filter_size", 2048)
  return hp


@registry.register_problem
class TextAdventure64(text_problems.Text2TextProblem):
  """Predict next line of poetry from the last line. From Gutenberg texts."""

  @property
  def approx_vocab_size(self):
    return 2**18  # ~250k

  @property
  def is_generate_per_split(self):
    # generate_data will shard the data into TRAIN and EVAL for us.
    return False

  @property
  def dataset_splits(self):
    """Splits of data to produce and number of output shards for each."""
    # 10% evaluation data
    return [{
        "split": problem.DatasetSplit.TRAIN,
        "shards": 8,
    }, {
        "split": problem.DatasetSplit.EVAL,
        "shards": 1,
    }, {
        "split": problem.DatasetSplit.TEST,
        "shards": 1,
    }]

  @property
  def vocab_type(self):
      return text_problems.VocabType.SUBWORD

  def generate_samples(self, data_dir, tmp_dir, dataset_split):
    del data_dir
    del tmp_dir
    del dataset_split

    with open("/home/ericthewry/courses/nlp/autoplay/csv_64_data/all_data.csv") as data_fp:
        if_reader = csv.reader(data_fp, delimiter=",", quotechar="\"")        
    
        for game_text, user_response in if_reader:
            yield {
                "inputs": game_text,
                "targets": user_response,
            }
            
