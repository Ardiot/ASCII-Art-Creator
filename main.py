""" Created by Carlos Garcia @Ardiot """


from ascii import ascii_art


def main():

    ascii_local_path = ascii_art(
        "dibujo.jpeg",
        60,
        45,
        edge_detection=False,
    )
    ascii_url = ascii_art(
        "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/71SVrsU3ZOL._SL1500_.jpg",
        60,
        45,
        edge_detection=False,
    )

    print(ascii_local_path.get_string("high"))

    print(
        ascii_url.get_string(
            encode_dictionary="abcdefghijklmnopqrstuvwxyz", space_between_chr=0
        )
    )


if __name__ == "__main__":
    main()
