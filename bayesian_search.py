#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 16:10:57 2025

@author: diastudent1
"""
from pipeline import Pipeline
from skopt import gp_minimize
from skopt.space import Real
class Bayesian_search_sigmas:
    def __init__(self):
        self.run_no = 0
        self.full_pipeline = Pipeline()
    def objective(self, sigmas):
        
        sigma1, sigma2, sigma3 = sigmas
        
        # Optional: penalize invalid sigma combinations
        if sigma1 == sigma2 or sigma1 == sigma3 or sigma2 == sigma3:
            return 1e6
        
        try:
            score = self.full_pipeline.full_pipeline(
                script_path='/home/diastudent1/Workspace/isis/register/Pipeline.csh',
                run_no= self.run_no,       # or increment dynamically
                deg_bg=5,
                deg_g1=5,
                deg_g2=2,
                deg_g3=4,
                sigma1=sigma1,
                sigma2=sigma2,
                sigma3=sigma3
            )
            self.run_no = self.run_no + 1
            return -score  # negative because gp_minimize minimizes
        except Exception as e:
            print(f"Pipeline failed: {e}")
            return 1e6
    
    
    
    
    def bayesian_sigma_search():
    
        search_space = [
            Real(0.5, 7.0, name='sigma1'),
            Real(0.5, 12.0, name='sigma2'),
            Real(0.5, 14.0, name='sigma3')
        ]
        
        result = gp_minimize(
            func= Bayesian_search_sigmas.objective,
            dimensions= search_space,
            acq_func="EI",      # Expected Improvement (popular choice)
            n_calls=20,         # Total function evaluations
            n_initial_points=5, # Random starting points
            random_state=42
        )
        
        best_sigmas = result.x
        best_score = -result.fun  # negate to recover original score

        return best_score, best_sigmas