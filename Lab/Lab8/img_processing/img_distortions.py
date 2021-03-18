from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tensorflow.python.framework import tensor_shape

def should_distort_images(flip_left_right, random_crop, random_scale,
                          random_brightness):
    """Whether any distortions are enabled, from the input flags.

    Args:
      flip_left_right: Boolean whether to randomly mirror images horizontally.
      random_crop: Integer percentage setting the total margin used around the
      crop box.
      random_scale: Integer percentage of how much to vary the scale by.
      random_brightness: Integer range to randomly multiply the pixel values by.

    Returns:
      Boolean value indicating whether any distortions should be applied.
    """
    return (flip_left_right or (random_crop != 0) or (random_scale != 0) or
            (random_brightness != 0))


def add_input_distortions(flip_left_right, random_crop, random_scale,
                          random_brightness, input_width, input_height,
                          input_depth, input_mean, input_std):
    """Creates the operations to apply the specified distortions.

    During training it can help to improve the results if we run the images
    through simple distortions like crops, scales, and flips. These reflect the
    kind of variations we expect in the real world, and so can help train the
    model to cope with natural data more effectively. Here we take the supplied
    parameters and construct a network of operations to apply them to an image.

    Cropping
    ~~~~~~~~

    Cropping is done by placing a bounding box at a random position in the full
    image. The cropping parameter controls the size of that box relative to the
    input image. If it's zero, then the box is the same size as the input and no
    cropping is performed. If the value is 50%, then the crop box will be half the
    width and height of the input. In a diagram it looks like this:

    <       width         >
    +---------------------+
    |                     |
    |   width - crop%     |
    |    <      >         |
    |    +------+         |
    |    |      |         |
    |    |      |         |
    |    |      |         |
    |    +------+         |
    |                     |
    |                     |
    +---------------------+

    Scaling
    ~~~~~~~

    Scaling is a lot like cropping, except that the bounding box is always
    centered and its size varies randomly within the given range. For example if
    the scale percentage is zero, then the bounding box is the same size as the
    input and no scaling is applied. If it's 50%, then the bounding box will be in
    a random range between half the width and height and full size.

    Args:
      flip_left_right: Boolean whether to randomly mirror images horizontally.
      random_crop: Integer percentage setting the total margin used around the
      crop box.
      random_scale: Integer percentage of how much to vary the scale by.
      random_brightness: Integer range to randomly multiply the pixel values by.
      graph.
      input_width: Horizontal size of expected input image to model.
      input_height: Vertical size of expected input image to model.
      input_depth: How many channels the expected input image should have.
      input_mean: Pixel value that should be zero in the image for the graph.
      input_std: How much to divide the pixel values by before recognition.

    Returns:
      The jpeg input layer and the distorted result tensor.
    """

    jpeg_data = tf.placeholder(tf.string, name='DistortJPGInput')
    decoded_image = tf.image.decode_jpeg(jpeg_data, channels=input_depth)
    decoded_image_as_float = tf.cast(decoded_image, dtype=tf.float32)
    decoded_image_4d = tf.expand_dims(decoded_image_as_float, 0)
    margin_scale = 1.0 + (random_crop / 100.0)
    resize_scale = 1.0 + (random_scale / 100.0)
    margin_scale_value = tf.constant(margin_scale)
    resize_scale_value = tf.random_uniform(tensor_shape.scalar(),
                                           minval=1.0,
                                           maxval=resize_scale)
    scale_value = tf.multiply(margin_scale_value, resize_scale_value)
    precrop_width = tf.multiply(scale_value, input_width)
    precrop_height = tf.multiply(scale_value, input_height)
    precrop_shape = tf.stack([precrop_height, precrop_width])
    precrop_shape_as_int = tf.cast(precrop_shape, dtype=tf.int32)
    precropped_image = tf.image.resize_bilinear(decoded_image_4d,
                                                precrop_shape_as_int)
    precropped_image_3d = tf.squeeze(precropped_image, squeeze_dims=[0])
    cropped_image = tf.random_crop(precropped_image_3d,
                                   [input_height, input_width, input_depth])
    if flip_left_right:
        flipped_image = tf.image.random_flip_left_right(cropped_image)
    else:
        flipped_image = cropped_image
    brightness_min = 1.0 - (random_brightness / 100.0)
    brightness_max = 1.0 + (random_brightness / 100.0)
    brightness_value = tf.random_uniform(tensor_shape.scalar(),
                                         minval=brightness_min,
                                         maxval=brightness_max)
    brightened_image = tf.multiply(flipped_image, brightness_value)
    offset_image = tf.subtract(brightened_image, input_mean)
    mul_image = tf.multiply(offset_image, 1.0 / input_std)
    distort_result = tf.expand_dims(mul_image, 0, name='DistortResult')
    return jpeg_data, distort_result
