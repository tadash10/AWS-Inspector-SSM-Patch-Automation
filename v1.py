import boto3

# Initialize AWS clients
ssm_client = boto3.client('ssm')
inspector_client = boto3.client('inspector')

# Define the EC2 instances to scan (you can obtain this list from your AWS environment)
instance_ids = ['i-XXXXXXXXXXXXX', 'i-YYYYYYYYYYYYY']

# Step 1: Start an Inspector assessment run
def start_inspector_assessment():
    response = inspector_client.start_assessment_run(
        assessmentTemplateArn='YourAssessmentTemplateARN',
        assessmentRunName='YourAssessmentRunName'
    )
    return response['assessmentRunArn']

# Step 2: Wait for Inspector assessment run to complete
def wait_for_inspector_completion(assessment_run_arn):
    while True:
        response = inspector_client.describe_assessment_runs(
            assessmentRunArns=[assessment_run_arn]
        )
        status = response['assessmentRuns'][0]['status']
        
        if status == 'COMPLETED':
            break
        elif status == 'FAILED' or status == 'CANCELED':
            raise Exception(f'Inspector assessment run failed or was canceled. Status: {status}')
        
        print(f'Inspector assessment run status: {status}')
    
# Step 3: Get a list of missing patches and vulnerabilities
def get_vulnerabilities():
    response = inspector_client.list_findings(
        assessmentRunArns=[assessment_run_arn],
        filter={'severities': ['High', 'Medium']}  # Adjust severity filters as needed
    )
    return response['findingArns']

# Step 4: Schedule patching activities using AWS Systems Manager
def schedule_patching(instance_id):
    response = ssm_client.create_maintenance_window(
        Name='PatchWindowForInstance',
        Schedule='cron(0 2 ? * SUN *)',  # Adjust the schedule as needed
        Duration=2,  # Adjust the duration as needed
        Cutoff=1,
        AllowUnassociatedTargets=True,
        WindowTargets=[
            {
                'Key': 'InstanceIds',
                'Values': [instance_id]
            },
        ],
    )
    return response['WindowId']

if __name__ == "__main__":
    assessment_run_arn = start_inspector_assessment()
    print("Inspector assessment run started.")
    wait_for_inspector_completion(assessment_run_arn)
    print("Inspector assessment run completed.")
    
    for instance_id in instance_ids:
        patching_window_id = schedule_patching(instance_id)
        print(f"Scheduled patching window {patching_window_id} for instance {instance_id}.")
    
    vulnerabilities = get_vulnerabilities()
    print(f"List of vulnerabilities: {vulnerabilities}")
