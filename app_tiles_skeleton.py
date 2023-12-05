import numpy as np
import pandas as pd
import cv2
import random
from pandas import read_csv

TILE_SIZE = 32

MARKET = """
##################
##..............##
#D..Dd..ds..sF..F#
#D..Dd..ds..sF..F#
#D..Dd..ds..sF..F#
#D..Dd..ds..sF..F#
#D..Dd..ds..sF..F#
##..............##
##..C#..C#..C#..##
##..##..##..##..##
##..............##
##############EE##
""".strip()


class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tiles  : a numpy array containing the tile images
        """
        self.tiles=tiles
        self.contents=[list(row) for row in layout.split("\n")]
        self.xsize=len(self.contents[0])
        self.ysize=len(self.contents)
        self.image=np.zeros((self.ysize*TILE_SIZE, self.xsize*TILE_SIZE, 3), dtype=np.uint8)
        self.prepare_map()

    def extract_tile(self, row, col):
        y=(row-1)*TILE_SIZE
        x=(col-1)*TILE_SIZE
        return self.tiles[y:y+TILE_SIZE, x:x+TILE_SIZE]

    def get_tile(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return self.extract_tile(1, 1)
        elif char == "E":  # entrance
            return self.extract_tile(8, 4)
        elif char == "C":  # checkout
            return self.extract_tile(3, 9)
        elif char == "F":  # frute
            return self.extract_tile(8, 11)
        elif char == "s":  # spices
            return self.extract_tile(7, 10)
        elif char == "d":  # dairy
            return self.extract_tile(1, 11)
        elif char == "D":  # drinks
            return self.extract_tile(7, 14)
        else:
            return self.extract_tile(2, 3)

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for row, line in enumerate(self.contents):
            for col, char in enumerate(line):
                bm = self.get_tile(char)
                y = row*TILE_SIZE
                x = col*TILE_SIZE
                self.image[y:y+TILE_SIZE, x:x+TILE_SIZE] = bm

    def background_create(self, frame, offset=50):
        """
        customer_goes the image into a frame
        """
        frame[offset:offset+self.image.shape[0], offset:offset+self.image.shape[1]] = self.image
        


class CustomerMap:
    def __init__(self, terrain_map, image):
        self.terrain_map = terrain_map
        self.image = image
        self.x = 0
        self.y = 0

    def customer_go(self, frame, location, offset=50):
        if location == "dairy":
            self.x = random.choice([6, 7])
            self.y = random.choice([2, 3, 4, 5, 6])
        elif location == "drinks":
            self.x = random.choice([2, 3])
            self.y = random.choice([2, 3, 4, 5, 6])
        elif location == "fruit":
            self.x = random.choice([14, 15])
            self.y = random.choice([2, 3, 4, 5, 6])
        elif location == "spices":
            self.x = random.choice([10, 11])
            self.y = random.choice([2, 3, 4, 5, 6])
        elif location == "checkout":
            self.x = random.choice([5, 9, 13])
            self.y = random.choice([8, 9])
        elif location == "entrance":
            self.x = random.choice([14, 15])
            self.y = random.choice([11])
        
        x_pos=offset+self.x*TILE_SIZE
        y_pos=offset+self.y*TILE_SIZE
        frame[y_pos:y_pos+self.image.shape[0], x_pos:x_pos+self.image.shape[1]] = self.image




if __name__ == "__main__":
    background = np.zeros((500, 700, 3), np.uint8)
    tiles = cv2.imread("./images/tiles.png")
    simulated_table = pd.read_csv('./simulated_market_table.csv', parse_dates=["timestamp"], date_parser=pd.to_datetime)
    opening = simulated_table["timestamp"].min()

    customer_figure = cv2.imread("./images/customer.png")
    customer_figure = cv2.resize(customer_figure, (TILE_SIZE, TILE_SIZE))
    market = SupermarketMap(MARKET, tiles)
    customer = CustomerMap(market, customer_figure)

    unique_timestamps = simulated_table["timestamp"].unique()

    for timestamp in unique_timestamps:
        frame = background.copy()
        market.background_create(frame)

        customers_at_time = simulated_table[simulated_table["timestamp"] == timestamp]
        for _, row in customers_at_time.iterrows():
            customer_location = row["location"]
            print("time:", timestamp, "customer_no:", row["customer_no"])
            print(customer_location)
            customer.customer_go(frame, customer_location)
            cv2.imshow("showframe", frame)
            cv2.waitKey(400)
          
    cv2.destroyAllWindows()