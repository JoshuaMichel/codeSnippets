# Provided by consultants and edited by me
# This script interacts with AWS Bedrock LLM models and sends a prompt and receives the response.

import boto3
import json
import os
import sys

module_path = ".."
sys.path.append(os.path.abspath(module_path))
from utils import bedrock, print_ww
from langchain import PromptTemplate
from langchain.llms.bedrock import Bedrock

os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
boto3_bedrock = bedrock.get_bedrock_client(os.environ.get('BEDROCK_ASSUME_ROLE', None))

from langchain.llms.bedrock import Bedrock

def build_chain():  
    inference_modifier = {'max_tokens_to_sample':4096, 
                      "temperature":0.5,
                      "top_k":250,
                      "top_p":1,
                      "stop_sequences": ["\n\nHuman"]
                     }

    textgen_llm = Bedrock(model_id = "anthropic.claude-v1",
                    client = boto3_bedrock, 
                    model_kwargs = inference_modifier 
                    )



    # Create a prompt template that has multiple input variables
    multi_var_prompt = PromptTemplate(
    input_variables=["customerServiceManager", "customerName", "feedbackFromCustomer"], 
    template="""Create an apology email from the Service Manager {customerServiceManager} to {customerName}. 
    in response to the following feedback that was received from the customer: {feedbackFromCustomer}.
    """
    )

    # Pass in values to the input variables
    prompt = multi_var_prompt.format(customerServiceManager="Bob", 
                                 customerName="John Doe", 
                                 feedbackFromCustomer="""Hello Bob,
                                 I am very disappointed with the recent experience I had when I called your customer support.
                                 I was expecting an immediate call back but it took three days for us to get a call back.
                                 The first suggestion to fix the problem was incorrect. Ultimately the problem was fixed after three days.
                                 We are very unhappy with the response provided and may consider taking our business elsewhere.
                                 """
                                 )
    num_tokens = textgen_llm.get_num_tokens(prompt)
    print(f"Our prompt has {num_tokens} tokens")
    response = textgen_llm(prompt)
    email = response[response.index('\n')+1:]  
    print_ww(email)
    return email