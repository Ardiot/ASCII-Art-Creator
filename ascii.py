""" Created by Carlos Garcia @Ardiot """


import numpy as np
from PIL import Image, ImageFilter
import validators
import os
import requests


class ascii_art:
    def __init__(self, path: str, widht: int, lenght: int, edge_detection=True) -> None:
        """Constructor for ascii

        Args:
            path (str): Path or url to an image
            widht (int): Number of characters in the x axis
            lenght (int): Number of characters in the y axis
            edge_detection (bool, optional): If True, images will be procesed with an edge detector

        Raises:
            Exception: UNABLE to DOWNLOAD PICTURE from if It can not dddownload the picture from the url
            Exception: UNABLE to OPEN IMAGE if Image can open the image
            Exception: UNABLE to FIND path  if image that not exists
        """
        if validators.url(path):
            try:
                self.image = Image.open(requests.get(path, stream=True).raw)
            except:
                raise Exception(
                    f"\033[0;31;40m UNABLE \033[0m to DOWNLOAD PICTURE from {path} "
                )

        else:
            if os.path.exists(path):
                self.path = path
                try:
                    self.image = Image.open(self.path)
                except:
                    raise Exception(f"\033[0;31;40mUNABLE \033[0m to OPEN IMAGE ")

            else:
                raise Exception(f"\033[0;31;40mUNABLE \033[0m to FIND path {path} ")

        if self.image != None:

            self.edge_detection = edge_detection
            self.num_char_width = widht
            self.num_char_lenght = lenght
            self.pixel_matrix = []
            self.pixel_matrix_reduce = []
            self.width, self.height = self.image.size

            self.process()
            self.reduce()

    def process(self):
        """
        First it will transform picture into a grey-scale picture. After this, Image will be
        processes with an edge detector.
        """

        self.image = self.image.convert("L")

        if self.edge_detection:
            self.image = self.image.filter(ImageFilter.FIND_EDGES)

        # Dump all pixel from the image to self.pixel_matrix array
        self.pixel_matrix = np.asarray(self.image)

    def reduce(self):
        """
        It will reduce the original (self.width x self.height) picture to a (self.num_char_width x self.num_char_length) matrix.
        It does a simple average.

        TODO Add more types of reduce
        """
        W = self.width
        L = self.height

        n = W // self.num_char_width
        m = L // self.num_char_lenght

        for num_of_row_block in range(self.num_char_lenght):
            aux_line = []
            for num_of_column_block in range(self.num_char_width):
                average_color = 0
                for i in range(m):
                    for j in range(n):
                        average_color += self.pixel_matrix[i + (num_of_row_block * m)][
                            j + (num_of_column_block * n)
                        ]
                aux_line.append(average_color // (n * m))
            self.pixel_matrix_reduce.append(aux_line)

    def get_string(self, encode_dictionary="medium", space_between_chr=0):
        """
        Return the ascii-art in a raw string
        """

        if encode_dictionary in ascii_art.default_dictionary:
            dictionary = ascii_art.default_dictionary[encode_dictionary]
        else:
            dictionary = encode_dictionary

        str_representation = ""
        dictionary_length = len(dictionary)

        for line_of_pixels in self.pixel_matrix_reduce:
            for pixel in line_of_pixels:
                str_representation += dictionary[
                    self.map_range(pixel, 0, 256, dictionary_length - 1, 0)
                ]
                str_representation += str(" " * space_between_chr)
            str_representation += "\n"
        return str_representation

    def map_range(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    default_dictionary = {
        "medium": "@MBHENR#KWXDFPQASUZbdehx*8Gm&04LOVYkpq5Tagns69owz$CIu23Jcfry%1v7l+it[] {}?j|()=~!-/<>\"^_';,:` ",
        "high": "@MBHENR#KWXDFPQASUZbdehx*8Gm&04LOVYkpq5Tagns69owz$CIu23Jcfry%1v7l+it[]{}?j|()=~!-/<>\"^_';        ",
        "medium_b": "@MBHENR#KWXDFPQASUZbdehx*8Gm&04LOVYkpq5Tagns69owz$CIu23Jcfry%1v7l+it[] {}?j|()=~!-/<>\"^_';,:`.",
        "high_b": "@MBHENR#KWXDFPQASUZbdehx*8Gm&04LOVYkpq5Tagns69owz$CIu23Jcfry%1v7l+it[]{}?j|()=~!-/<>\"^_';.........",
        "highest": "                   KWXDFPQASUZbdehx                 ",
    }
