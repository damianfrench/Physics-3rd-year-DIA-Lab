import subprocess
import numpy as np
import pandas as pd

# -------------------------
# Helper functions
# -------------------------
class Pipeline:
    @staticmethod
    def polynomial_coefficients(order):
        """Compute the number of coefficients for a 2D polynomial of given order."""
        order = float(order)
        return (order + 1) * (order + 2) / 2
    @staticmethod
    def compute_free_parameters(config):
        """Compute number of free parameters given a config dict."""
        df = pd.DataFrame([config])
        cols = [
            'deg_bg', 'deg_gauss1', 'deg_gauss2', 'deg_gauss3',
            'ngauss', 'sigma_gauss1', 'sigma_gauss2', 'sigma_gauss3'
        ]
        for col in cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
        total = (
            Pipeline.polynomial_coefficients(df['deg_bg'])
            + Pipeline.polynomial_coefficients(df['deg_gauss1'])
            + Pipeline.polynomial_coefficients(df['deg_gauss2'])
            + Pipeline.polynomial_coefficients(df['deg_gauss3'])
            + df['ngauss']
        )
        return int(total.iloc[0])
    
    @staticmethod               
    def parse_stats(run_no):
        stats_path = f'/home/diastudent1/Workspace_DG2/run{run_no}/stats.txt'
        """Parse the output stats file and return mean and scatter."""
        try:
            df = pd.read_csv(stats_path, delimiter=' ', header=None)
            df = df.drop(columns=[0, 2]).rename(columns={1: 'mean', 3: 'scatter'})
            mean = df['mean']
            scatter = df['scatter']
            return mean, scatter
        except Exception as e:
            print(f"Error parsing stats: {e}")
            raise
    @staticmethod   
    def dia_score(mean, scatter, n_free_parameters):
        """Compute custom DIA score (higher is better)."""
        weights = 1 / scatter ** 2
        weighted_mean = np.sum(weights + mean) / np.sum(weights)
        weighted_scatter = 1 / np.sqrt(np.sum(weights))
    
        min_mean = 0.33231
        max_mean = 0.99769
        min_scatter = 0.28085
        max_scatter = 0.87852
    
        norm_mean = (weighted_mean - min_mean) / (max_mean - min_mean)
        norm_scatter = (weighted_scatter - min_scatter) / (max_scatter - min_scatter)
    
        score = (1 / norm_mean) + (1 / norm_scatter) - n_free_parameters / (100 - n_free_parameters)
        return score


    @staticmethod
    def full_pipeline(run_no=None, deg_bg=None, deg_g1=None, deg_g2=None, deg_g3=None, sigma1=None, sigma2=None, sigma3=None):
        """Run the Pipeline C-shell script with the provided parameters."""

        script_path='/home/diastudent1/Workspace/isis/register/pipeline.csh'
        # Check if all required parameters are provided
        if None in [run_no, deg_bg, deg_g1, deg_g2, deg_g3, sigma1, sigma2, sigma3]:
            raise ValueError("All parameters (run_no, deg_bg, deg_g1, deg_g2, deg_g3, sigma1, sigma2, sigma3) must be provided.")
        if sigma1 == sigma2 or sigma1 == sigma3 or sigma2 == sigma3:
            return np.inf  # Return a very high value if sigmas are equal (invalid)
        # Run the Pipeline C-shell script with the provided arguments
        subprocess.run(['csh', script_path, str(run_no), str(deg_bg), str(deg_g1), str(deg_g2), str(deg_g3), str(sigma1), str(sigma2), str(sigma3)], check=True,  cwd=script_path)
    
        # Parse the results
        mean, scatter = Pipeline.parse_stats(run_no)
        free_params = Pipeline.compute_free_parameters('/home/diastudent1/Workspace_DG2/run{run_no}/config_used')
        results = Pipeline.dia_score(mean, scatter, free_params)
        
        return results
