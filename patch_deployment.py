import time

def roll_patch_deployment(instance_ids, batch_size=2):
    # Function to implement rolling patch deployments to minimize downtime
    for i in range(0, len(instance_ids), batch_size):
        batch = instance_ids[i:i + batch_size]
        for instance_id in batch:
            # Apply patches to instances in this batch
            time.sleep(30)  # Simulated patching delay
