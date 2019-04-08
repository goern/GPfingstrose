import requests
import numpy as np
from PIL import Image
from io import BytesIO


def create_request(array):
    return '{"instances": %s}' % array

def image_downloader(image_url):
    response = requests.get(image_url)
    pil_image = Image.open(BytesIO(response.content))
    return pil_image

def image_to_array(pil_image, shape=None):
    ################### Remove next line for the final model ###############
    pil_image = pil_image.convert(mode="L")
    ########################################################################

    img_array = np.array(pil_image)
    if shape:
        img_array = img_array.reshape(shape)
    return img_array

def tf_request(server_url, image_url):

    # Download the image using the given url and resize it to 28x28px
    input_image = image_downloader(image_url).resize((28, 28))

    # Convert the image to a pixel np array and then flatten it to a size 784 list
    image_array = image_to_array(input_image, shape=(784)).tolist()

    # Create a string request from the array to send it to the tensorflow model
    new_request = create_request(str(image_array))

    # Post the request to the tensorflow serving api
    response = requests.post(server_url, new_request)
    response.raise_for_status()

    # Prediction response from the api
    prediction_list = response.json()['predictions'][0]

    # return the index with the highest value of likelihood
    return prediction_list.index(max(prediction_list))
