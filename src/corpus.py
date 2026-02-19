# Importamos librerías
import json
import requests
import os
from os import makedirs
from os.path import join, exists
from datetime import date, timedelta
import ast
import workspace
import sys
from guardian import Guardian

def __main__():
    os.chdir("..")
    # retrieve the workspace path
    workspace.set_workspace_path(os.getcwd())

    start_date = date(2026,1,1)
    end_date = date(2026,2,1)

    # create object for the Guardian API
    g = Guardian(start_date, end_date)
    # retrieve articles from the start date to the end date
    g.fetch_articles()

__main__()
