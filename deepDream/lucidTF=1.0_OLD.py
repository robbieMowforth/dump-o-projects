#ONLY WORKS IF YOU HAVE TENSORFLOW VER 1.x.x INSTALLED

import numpy as np
import tensorflow as tf
assert tf.__version__.startswith('1')

import lucid.modelzoo.vision_models as models
from lucid.misc.io import show
import lucid.optvis.objectives as objectives
import lucid.optvis.param as param
import lucid.optvis.render as render
import lucid.optvis.transform as transform

model = models.InceptionV1()
model.load_graphdef()

dream_img = render.render_vis(model, "mixed4a_pre_relu:476")

print(dream_img)

tf.keras.preprocessing.image.save_img('dream_img'+'.png',dream_img)
