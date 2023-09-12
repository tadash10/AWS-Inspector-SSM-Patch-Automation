import os

# Load configuration from environment variables
ASSESSMENT_TEMPLATE_ARN = os.getenv('ASSESSMENT_TEMPLATE_ARN', 'YourDefaultTemplateARN')
ASSESSMENT_RUN_NAME = os.getenv('ASSESSMENT_RUN_NAME', 'YourDefaultRunName')
INSTANCE_IDS = os.getenv('INSTANCE_IDS', 'i-XXXXXXXXXXXXX,i-YYYYYYYYYYYYY').split(',')
