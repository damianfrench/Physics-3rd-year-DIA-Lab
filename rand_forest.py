#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 16:47:38 2025

@author: diastudent1
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 16:10:57 2025

@author: diastudent1
"""
import pipeline
from skopt import forest_minimize
from skopt.space import Real

class Rand_forest:
    def __init__(self, start_run_no=0):
        self.run_no = start_run_no

    def objective(self, sigmas):
        sigma1, sigma2, sigma3 = sigmas

        # Penalize invalid sigma combinations
        if sigma1 == sigma2 or sigma1 == sigma3 or sigma2 == sigma3:
            return 1e6

        try:
            score = pipeline.full_pipeline(
                script_path='~/DIAphotometry/register/Pipeline.csh',
                run_no=self.run_no,
                deg_bg=5,
                deg_g1=5,
                deg_g2=2,
                deg_g3=4,
                sigma1=sigma1,
                sigma2=sigma2,
                sigma3=sigma3
            )
            self.run_no += 1
            return -score  # Minimize negative score
        except Exception as e:
            print(f"Pipeline failed: {e}")
            return 1e6

    def random_forest_sigma_search(self, n_calls=20, n_initial_points=5):
        search_space = [
            Real(0.5, 7.0, name='sigma1'),
            Real(0.5, 12.0, name='sigma2'),
            Real(0.5, 14.0, name='sigma3')
        ]

        result = forest_minimize(
            func=self.objective,      # Note: instance method
            dimensions=search_space,
            n_calls=n_calls,
            n_initial_points=n_initial_points,
            random_state=42
        )

        best_sigmas = result.x
        best_score = -result.fun  # convert back to original score

        return best_score, best_sigmas
