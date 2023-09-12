import boto3

ssm_client = boto3.client('ssm')

def get_parameter(parameter_name):
    response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
    return response['Parameter']['Value']

def set_parameter(parameter_name, parameter_value):
    ssm_client.put_parameter(Name=parameter_name, Value=parameter_value, Type='SecureString')
