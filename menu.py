import sys
import time
import select
from closest_cluster import *


def update_database_periodically():
    # Simulating fetching, processing, and updating data
    print("Fetching data...")
    time.sleep(2)
    print("Data fetched successfully.")
    print("Processing data...")
    time.sleep(2)
    print("Data processed successfully.")
    print("Updating database...")
    time.sleep(5)
    print("Database updated successfully.")
    return time.time()
    

def find_cluster():
    message = input("Enter keywords or a message: ")
    input_word, closest_cluster, top_words = closest_find(message)
    print("Finding closest cluster..")
    print(f"The closest cluster for the word '{input_word}' is Cluster {closest_cluster}")    
    print(f"Top 10 words in Cluster {closest_cluster}: {', '.join(top_words)}")
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python menu.py <interval>")
        sys.exit(1)

    global interval
    interval = int(sys.argv[1]) * 60

    start_wait = update_database_periodically()

    while True:
        
        # Take user input as long as DB is waiting for next update
        while time.time() < start_wait + interval:  
            
            # Wait for the given interval of time for user to give an input
            print("\nEnter your choice:\n1. Find a cluster\n2. Quit\n", end='', flush=True)
            input_received = select.select([sys.stdin], [], [], interval - (time.time() - start_wait))[0]   
            
            if input_received:
                choice = sys.stdin.readline().strip()
                if choice == '1':
                    find_cluster()
                elif choice=='2':
                    sys.exit("Bye!")

        # Update DB and wait time
        start_wait = update_database_periodically()
        


