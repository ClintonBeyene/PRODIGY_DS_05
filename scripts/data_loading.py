import kagglehub
import time

# Set the maximum number of retries and the retry delay
max_retries = 3
retry_delay = 10  # seconds

# Download the dataset with retries
for attempt in range(max_retries):
    try:
        path = kagglehub.dataset_download("sobhanmoosavi/us-accidents")
        print("Path to dataset files:", path)
        break
    except Exception as e:
        print(f"Error downloading dataset (attempt {attempt+1}/{max_retries}): {str(e)}")
        time.sleep(retry_delay)
else:
    print("Failed to download dataset after {} attempts. Please try again later.".format(max_retries))