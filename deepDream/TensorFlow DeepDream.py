#WORKING LOCAL MODEL
#TODO:
#1. Look into code further, understand how to tweak though google tutorial
#2. Intergrate with discord bot?
#3. Make it human readable
#4. play around with nodes and octaves more

#ONLY WORKS IF YOU HAVE TENSORFLOW VER 2.3.x INSTALLED

#imports used for AI
import tensorflow as tf
import numpy as np
import matplotlib as mpl
from tensorflow.keras.preprocessing import image

#imports used for image and video processing
import IPython.display as display
import PIL.Image
import os
import cv2


# Download an image and read it into a NumPy array.
def download(url, max_dim=None):
  name = url.split('/')[-1]
  image_path = tf.keras.utils.get_file(name, origin=url)
  img = PIL.Image.open(image_path)
  if max_dim:
    img.thumbnail((max_dim, max_dim))
  return np.array(img)

def localSetImg(img, max_dim=None):
  img = PIL.Image.open('input/'+img)
  if max_dim:
    img.thumbnail((max_dim, max_dim))
  return np.array(img)

# Normalize an image
def deprocess(img):
  img = 255*(img + 1.0)/2.0
  return tf.cast(img, tf.uint8)

#this is the varible that takes the image, must be as a accessible online url to image
url = 'https://storage.googleapis.com/download.tensorflow.org/example_images/YellowLabradorLooking_new.jpg'
# Downsizing the image makes it easier to work with.
#Entry point to use an image taken from a URL
original_img = download(url, max_dim=500)

#creation of the trained AI
#We are using pre-downloaded weights stored locally (see: weights=)
#All pre-trained weights/models are stored in folder weights
#Due to the nature of the code using different models doesn't work rn
#Everything is dependant on the InceptionV3 notop model
base_model = tf.keras.applications.InceptionV3(
  include_top=False,
  weights='weights/inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5'
)

# Maximize the activations of these layers
names = ['mixed3', 'mixed5']
layers = [base_model.get_layer(name).output for name in names]

# Create the feature extraction model
dream_model = tf.keras.Model(inputs=base_model.input, outputs=layers)

#calculate loss, stops large layers outweighting small layers
#we aim to maximize loss due to deep dream
def calc_loss(img, model):
  # Pass forward the image through the model to retrieve the activations.
  # Converts the image into a batch of size 1.
  img_batch = tf.expand_dims(img, axis=0)
  layer_activations = model(img_batch)
  if len(layer_activations) == 1:
    layer_activations = [layer_activations]

  losses = []
  for act in layer_activations:
    loss = tf.math.reduce_mean(act)
    losses.append(loss)

  return  tf.reduce_sum(losses)

#gradient ascent
#enhances the patterns seen by the network
class DeepDream(tf.Module):
  def __init__(self, model):
    self.model = model

  @tf.function(
      input_signature=(
        tf.TensorSpec(shape=[None,None,3], dtype=tf.float32),
        tf.TensorSpec(shape=[], dtype=tf.int32),
        tf.TensorSpec(shape=[], dtype=tf.float32),)
  )
  def __call__(self, img, steps, step_size):
      print("Tracing")
      loss = tf.constant(0.0)
      for n in tf.range(steps):
        with tf.GradientTape() as tape:
          # This needs gradients relative to `img`
          # `GradientTape` only watches `tf.Variable`s by default
          tape.watch(img)
          loss = calc_loss(img, self.model)

        # Calculate the gradient of the loss with respect to the pixels of the input image.
        gradients = tape.gradient(loss, img)

        # Normalize the gradients.
        gradients /= tf.math.reduce_std(gradients) + 1e-8 
        
        # In gradient ascent, the "loss" is maximized so that the input image increasingly "excites" the layers.
        # You can update the image by directly adding the gradients (because they're the same shape!)
        img = img + gradients*step_size
        img = tf.clip_by_value(img, -1, 1)

      return loss, img

#creates the deep dream model
deepdream = DeepDream(dream_model)

#function which 'deep dreams' the image very simply
def run_deep_dream_simple(img, steps=100, step_size=0.01):
  # Convert from uint8 to the range expected by the model.
  img = tf.keras.applications.inception_v3.preprocess_input(img)
  img = tf.convert_to_tensor(img)
  step_size = tf.convert_to_tensor(step_size)
  steps_remaining = steps
  step = 0
  while steps_remaining:
    if steps_remaining>100:
      run_steps = tf.constant(100)
    else:
      run_steps = tf.constant(steps_remaining)
    steps_remaining -= run_steps
    step += run_steps

    loss, img = deepdream(img, run_steps, tf.constant(step_size))
    
    display.clear_output(wait=True)
    show(deprocess(img))
    print ("Step {}, loss {}".format(step, loss))

  result = deprocess(img)
  display.clear_output(wait=True)
  show(result)

  return result

#---------NEW CODE-------------########
#Missing the first new improvement used form the website deu to func usage
#^^ SEE BOTTOM OF CODE ^^#

#random shift of image
def random_roll(img, maxroll):
  # Randomly shift the image to avoid tiled boundaries.
  shift = tf.random.uniform(shape=[2], minval=-maxroll, maxval=maxroll, dtype=tf.int32)
  shift_down, shift_right = shift[0],shift[1] 
  img_rolled = tf.roll(tf.roll(img, shift_right, axis=1), shift_down, axis=0)
  return shift_down, shift_right, img_rolled

class TiledGradients(tf.Module):
  def __init__(self, model):
    self.model = model

  @tf.function(
      input_signature=(
        tf.TensorSpec(shape=[None,None,3], dtype=tf.float32),
        tf.TensorSpec(shape=[], dtype=tf.int32),)
  )
  def __call__(self, img, tile_size=512):
    shift_down, shift_right, img_rolled = random_roll(img, tile_size)

    # Initialize the image gradients to zero.
    gradients = tf.zeros_like(img_rolled)
    
    # Skip the last tile, unless there's only one tile.
    xs = tf.range(0, img_rolled.shape[0], tile_size)[:-1]
    if not tf.cast(len(xs), bool):
      xs = tf.constant([0])
    ys = tf.range(0, img_rolled.shape[1], tile_size)[:-1]
    if not tf.cast(len(ys), bool):
      ys = tf.constant([0])

    for x in xs:
      for y in ys:
        # Calculate the gradients for this tile.
        with tf.GradientTape() as tape:
          # This needs gradients relative to `img_rolled`.
          # `GradientTape` only watches `tf.Variable`s by default.
          tape.watch(img_rolled)

          # Extract a tile out of the image.
          img_tile = img_rolled[x:x+tile_size, y:y+tile_size]
          loss = calc_loss(img_tile, self.model)

        # Update the image gradients for this tile.
        gradients = gradients + tape.gradient(loss, img_rolled)

    # Undo the random shift applied to the image and its gradients.
    gradients = tf.roll(tf.roll(gradients, -shift_right, axis=1), -shift_down, axis=0)

    # Normalize the gradients.
    gradients /= tf.math.reduce_std(gradients) + 1e-8 

    return gradients

#check usage
get_tiled_gradients = TiledGradients(dream_model)

def run_deep_dream_with_octaves(img, steps_per_octave,
                                step_size, 
                                octaves,
                                octave_scale):

  base_shape = tf.shape(img)
  img = tf.keras.preprocessing.image.img_to_array(img)
  img = tf.keras.applications.inception_v3.preprocess_input(img)

  initial_shape = img.shape[:-1]
  img = tf.image.resize(img, initial_shape)
  for octave in octaves:
    # Scale the image based on the octave
    new_size = tf.cast(tf.convert_to_tensor(base_shape[:-1]), tf.float32)*(octave_scale**octave)
    img = tf.image.resize(img, tf.cast(new_size, tf.int32))

    for step in range(steps_per_octave):
      gradients = get_tiled_gradients(img)
      img = img + gradients*step_size
      img = tf.clip_by_value(img, -1, 1)

      if step % 10 == 0:
        display.clear_output(wait=True)
        print ("Octave {}, Step {}".format(octave, step))
    
  result = deprocess(img)
  return result

#START OF HAND_MADE CODE####################################################

dirPathInput = 'input/'

def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite(dirPathInput+str(count)+".jpg", image)# save frame as JPG file
    return hasFrames

check=True
while(check):
  videoCheck = input("Do you want to process a video or not?(Y,N): ")
  if videoCheck not in ['Y','N']:
    print('input wrong, try again/n')
    
  elif videoCheck == 'Y':
    vidcap = cv2.VideoCapture('video/START.mp4')  
    sec = 0
    frameRate = 0.05 #//it will capture image in each 0.05 second 20fps
    count=1
    success = getFrame(sec)
    while success:
      count = count + 1
      sec = sec + frameRate
      sec = round(sec, 2)
      success = getFrame(sec)

    check = False
      
  else: check = False

for i, entry in enumerate(os.listdir(dirPathInput)):
  print(str(i))
  print(entry)
  print(url)
  print(original_img)
  original_img = localSetImg(entry, max_dim=500)
  #ENTRY POINT FOR VARIBLE CHANGE#
  dream_img = run_deep_dream_with_octaves(img=original_img,
                                          step_size=0.01, #VAR
                                          steps_per_octave=500, #VAR
                                          octaves=range(-2,3), #VAR
                                          octave_scale=1.3) #VAR

  #video loop save
  tf.keras.preprocessing.image.save_img('output/dream_img'+str(i)+'.png',dream_img)

  

#creates the deep dream image
#dream_img = run_deep_dream_simple(img=original_img, 
                                  #steps=100, step_size=0.01)

#saves the deep dream image to the current directory
#tf.keras.preprocessing.image.save_img('dream_img.png',dream_img)

#---------NEW CODE-------------#
#improvement removed due to timeframe so that we could process archie

#import time
#start = time.time()

#OCTAVE_SCALE = 1.30

#img = tf.constant(np.array(original_img))
#base_shape = tf.shape(img)[:-1]
#float_base_shape = tf.cast(base_shape, tf.float32)

#for n in range(-2, 3):
 #new_shape = tf.cast(float_base_shape*(OCTAVE_SCALE**n), tf.int32)

  #img = tf.image.resize(img, new_shape).numpy()

  #img = run_deep_dream_simple(img=img, steps=50, step_size=0.01)

#display.clear_output(wait=True)
#img = tf.image.resize(img, base_shape)
#img = tf.image.convert_image_dtype(img/255.0, dtype=tf.uint8)
#show(img)

#end = time.time()
#end-start
