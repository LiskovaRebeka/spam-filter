from confmat import BinaryConfusionMatrix
import utils
import os

pos_tag = "SPAM"
neg_tag = "OK"


def compute_quality_for_corpus(corpus_dir):
    truth_dict = utils.read_classification_from_file(
                                os.path.join(corpus_dir, '!truth.txt'))
    prediction_dict = utils.read_classification_from_file(
                                os.path.join(corpus_dir, '!prediction.txt'))
    confusion_matrix = BinaryConfusionMatrix(pos_tag, neg_tag)
    confusion_matrix.compute_from_dicts(truth_dict, prediction_dict)

    conf_dict = confusion_matrix.as_dict()
    return quality_score(**conf_dict)


def quality_score(**args):
    true_values = args['tp'] + args['tn']
    false_values = 10*args['fp'] + args['fn']
    score = true_values / (true_values + false_values)
    return score
