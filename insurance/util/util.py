from importlib.resources import path
from insurance.constant import *
from insurance.exception import InsuranceException
import yaml
import os,sys
import pandas as pd
import numpy as np
import dill

def read_yaml_file(file_path)->dict:
    try:
        with open(file_path) as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise InsuranceException(e,sys) from e


def write_yaml_file(file_path:str,data:dict=None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise InsuranceException(e,sys)


def load_data(file_path:str,schema_file_path:str)->pd.DataFrame:
    try:
        dataset_schema=read_yaml_file(schema_file_path)
        schema=dataset_schema[SCHEMA_FILE_COLUMNS_KEY]
        dataframe=pd.read_csv(file_path)
        error_message=""

        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])
            else:
                error_message=f"{error_message} \nColumn: [{column}] is not in the schema"
        if len(error_message)>0:
            raise Exception(error_message)
        return dataframe
    except Exception as e:
        raise InsuranceException(e,sys) from e

def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise InsuranceException(e,sys) from e

def load_numpy_array_data(file_path:str)->np.array:
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise InsuranceException(e,sys) from e

def save_object(file_path:str,obj):
    try:
        """
        file_path:str
        obj:Any sort of object
        """
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
    except Exception as e:
        raise InsuranceException(e,sys) from e

def load_object(file_path:str):
    """
    file_path:str
    """
    try:
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise InsuranceException(e,sys) from e


