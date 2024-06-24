# HThis module if for automate the configuration reading and later use in each module 
# add in each module: from read_config import LIST_MODELS, DATA_FOLDER, LOG_LEVEL....

import os 
import json

# get parameters from config file
script_dir = os.path.dirname(os.path.realpath(__file__))
relative_config_path = os.path.join(script_dir, '..', 'conf', 'system_config.json')
config_path = os.path.abspath(relative_config_path)
with open(config_path, 'r') as file:
    config = json.load(file)

# get log parameters
if os.name == 'nt': # 'nt' stands for Windows
    DATA_FOLDER = config['windows_data_folder']  
    LOG_FILE = config['windows_log_file']   
elif os.name == 'posix': # 'posix' stands for Linux/Unix
    DATA_FOLDER = config['linux_data_folder']
    LOG_FILE = config['linux_log_file']
else:
    raise OSError("Unsupported operating system")

DB_NAME = config['db_name']
DB_USER = config['db_user']
DB_PASSWORD = config['db_password']
SCHEMA = config['schema']
LOG_LEVEL = config['log_level']
LIST_MODELS = config['list_models']

relative_prompt_path = os.path.join(script_dir, '..', 'conf', 'assistent-chunk-prompt.json')
prompt_path = os.path.abspath(relative_prompt_path)
with open(prompt_path, 'r') as file:
    prompt = json.load(file)

PROMPT_CHUNK_DESCRIPTION = prompt['description']
PROMPT_CHUNK_INSTRUCTIONS = prompt['instructions']
PROMPT_CHUNK_ADD_TO_PROMPT = prompt['add_to_prompt']

relative_prompt_path = os.path.join(script_dir, '..', 'conf', 'assistent-summ-prompt.json')
prompt_path = os.path.abspath(relative_prompt_path)
with open(prompt_path, 'r') as file:
    prompt = json.load(file)

PROMPT_SUMM_DESCRIPTION = prompt['description']
PROMPT_SUMM_INSTRUCTIONS = prompt['instructions']
PROMPT_SUMM_ADD_TO_PROMPT = prompt['add_to_prompt']


