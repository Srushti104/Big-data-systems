import os
import argparse
import tensorflow as tf
# import tensorflow.compat.v1 as tf
from IPython.display import Image

import retrain

# Have a look at the default values
# For the meaning of these values look at retrain_CNN.py:

FLAGS = argparse.Namespace()
# FLAGS.image_dir = ""
FLAGS.output_graph = './models/retrained_graph.pb'
FLAGS.output_labels = './models/output_labels.txt'
FLAGS.summaries_dir = '.\\summaries'
FLAGS.how_many_training_steps = 4000
FLAGS.learning_rate = 0.01
FLAGS.testing_percentage = 10
FLAGS.validation_percentage = 10
FLAGS.eval_step_interval = 10
FLAGS.train_batch_size = 100
FLAGS.test_batch_size = -1
FLAGS.validation_batch_size = 100
FLAGS.intermediate_store_frequency =10
FLAGS.print_misclassified_test_images = False
FLAGS.model_dir = "."
FLAGS.bottleneck_dir = "bottlenecks"
FLAGS.final_tensor_name = "final_result"
FLAGS.flip_left_right = False
FLAGS.random_crop = 0
FLAGS.random_scale = 0
FLAGS.random_brightness = 0
FLAGS.intermediate_output_graphs_dir ="."
FLAGS.architecture = "mobilenet_1.0_224"
# change default:
FLAGS.how_many_training_steps = 500
FLAGS.model_dir = "Mobilenet"
# FLAGS.summaries_dir = "C:\\to\\temp"
FLAGS.output_graph = "./models/retrained_graph_v2.pb"
FLAGS.output_labels = "./models/retrained_labels.txt"
FLAGS.image_dir = "ScrapedData-Acne-and-Rosacea-Photos/"

retrain.FLAGS = FLAGS

try:
    tf.compat.v1.app.run(main=retrain.main)
except:
    pass