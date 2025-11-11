#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 16:08:46 2025

@author: diastudent1
"""

#from bayesian_search import Bayesian_search_sigmas
from pipeline import Pipeline
class Main:
    def __init__(self):
        #self.bayesian_search = Bayesian_search_sigmas()
        self.full_pipeline = Pipeline()
    def main(self):
        #self.bayesian_search.Bayesian_sigma_search()
        self.full_pipeline.full_pipeline(script_path='/home/diastudent1/Workspace/isis/register/pipeline.csh', run_no=0, deg_bg=1, deg_g1=2, deg_g2=3, deg_g3=4, sigma1=1, sigma2=2, sigma3=3)
           
if __name__ == "__main__":
    program = Main()
    program.main()