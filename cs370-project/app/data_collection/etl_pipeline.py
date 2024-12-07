import os
from pymongo import MongoClient
from data_collection.helpers.download_utils import download_data
from data_collection.helpers.parse_ros2 import parse_ros2_docs

# MongoDB connection
client = MongoClient("mongodb://mongodb:27017")
db = client['rag_project']

# Download and parse ROS2 docs
def etl_pipeline():
    # Step 1: Download data
    ros2_url = "https://docs.ros.org/en/"
    ros2_raw_path = "/usr/src/app/data/raw/ros2/ros2_docs.html"
    download_data(ros2_url, ros2_raw_path)

    # Step 2: Parse data
    parsed_data = parse_ros2_docs(ros2_raw_path)

    # Step 3: Insert into MongoDB
    db.ros2.insert_one(parsed_data)
    print("Data inserted into MongoDB.")

if __name__ == "__main__":
    etl_pipeline()
