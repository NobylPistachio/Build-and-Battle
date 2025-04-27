from tqdm import tqdm
import time

tasks = ['loading data', 'processing images', 'training model', 'saving results']

with tqdm(total=len(tasks)) as pbar:
    for task in tasks:
        # Update the description next to the bar
        pbar.set_description(f"Current Task: {task}")

        # Write extra text below the bar
        tqdm.write(f"Started: {task}")

        time.sleep(1)  # simulate work
        pbar.update(1)

tqdm.write("All tasks completed!")



# def update_progress(task, list:tqdm):
#     list.set_description(f"{task}")
#     time.sleep(1)

# a = tqdm(tasks)

# for task in a:
#     update_progress(task, a)

