# DIA Photometry — 3rd Year Physics Lab  
  
This repo contains the code, lab report, and presentation from my 8-week lab on DIA photometry and gravitational microlensing.  
  
The experiment used difference imaging to detect variations in stellar flux, enabling identification of gravitational microlensing events — where a massive foreground object curves spacetime, focusing light from a distant background source. From the M31 bulge dataset, 4 microlensing events were identified and the lens mass determined for 2 of them. 

In ML terms, this project involved training a parameterised image model (the convolution kernel) on a sampled subset of the data, selecting the optimal model via a custom validation and scoring procedure across 8,500 hyperparameter configurations, and applying the best kernel to the full dataset for inference.
  
Further details can be found in the report   
  
## Repo Structure  
  
- code — Python and C-Shell scripts for hyperparameter search, image processing, and scoring  
- report — Full written report  
- presentation — Lab presentation slides  
  
## DIA Photometry  
  
Difference imaging works by subtracting a target image from a reference image built from a stack of high-quality frames. Because each image is taken under different seeing conditions, the reference is convolved with a spatially varying kernel to match the PSF of each target, along with a background term to normalise flux levels.  
  
The ideal solution would fit a unique kernel per pixel which is computationally infeasible. Instead, the kernel and background are expressed as linear combinations of basis functions, with coefficients solved by minimising the sum of squared residuals between reference and target. This reduces the problem to selecting the right basis functions and how many to use, a model selection problem analogous to cross-validation in machine learning.  
  
## Hyperparameter Optimisation  
  
Seven hyperparameters govern the basis space. To find the optimal configuration, an automated end-to-end pipeline (C-Shell) was built and run over several days, generating 8,500 hyperparameter configurations. Each configuration produced 10 difference images from randomly sampled target frames.  
  
After this pipeline, an analysis was done in python on the resultant images to determine the optimal set of hyperparameters.  
  
Image quality was quantified by mean and scatter (lower is better). Across the 10 images per configuration, inverse-variance weighted means and uncertainties were computed (weights = 1/σ²), yielding a summary statistic for each of the 8,500 configurations.  
  
The 7 hyperparameters split into 4 discrete and 3 continuous, optimised separately with literature values used to fix one group while the other was varied.  
  
### Scoring  
  
Two custom objective functions were designed to balance fit quality against model complexity, biasing against excess free parameters (N) to avoid overfitting.  
  
### Method 1  
  
```
S = (1/mean) + (1/scatter) - (N / (100 - N))

```
  
  
Scores were plotted against N and a cumulative improvement threshold algorithm applied to identify plateaus, which are regions where additional free parameters no longer meaningfully improved the score. This method tended to get trapped in local minima, motivating a second approach.  
  
### Method 2  
  
```
S = (1/mean) + (1/scatter) - 20N

```
  
  
The linear penalty coefficient (20) was chosen to bias selection toward the middle of the N range rather than simply minimising it. The threshold algorithm was modified to track gradient changes in S with respect to N, successfully identifying a stable plateau.  
