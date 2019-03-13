# Basic Credit Card Segmentation using K-Means Clustering

### What is this?

This repo contains work for a take-home assignment for an education/online media company. From completion of this assignment, I progressed to a technical walkthrough-style video interview. Later, I had an on-site, mostly non-technical final round. That was as far as I progressed.

### What was this take-home about?

For this assignment, I was asked to search for some datasets on Kaggle using a search term from a list of candidate terms (I chose 'customer segmentation') and ultimately identify a dataset to analyze a problem of my choosing.

I decided to use a hypothetical (I think?) Credit Card customer dataset to identify/describe different customer segments and discuss potential actions for the provider to take with each segment. Much more detail describing my choices and workflow is given in the notebook included here: **Short Credit Card Segmentation Exercise with K Means.ipynb**.

### Additional Notes

Although this particular assignment helped me advance in the process, there are areas where the analysis could very easily be improved:

* Imputation of missing values using the median is a bit too basic, and for the feature `MINMUM_PAYMENTS` I'm not convinced it was appropriate.
* I believe the feature `TENURE` should have been dropped before proceeding with any clustering analysis -- it appears to be a categorical feature masquerading as a numeric.
* Reproducibility might be an issue (although the resulting clusters will have the same general characteristics), even with specification of `random_state` -- might need to see if this can work better with `np.random.seed` or `np.random.RandomState`. Of course, K-Means [may not fully accommodate](https://stackoverflow.com/questions/25921762/changes-of-clustering-results-after-each-time-run-in-python-scikit-learn) such easy reproducibility. I also ought to have taken better care in my EDA to check the validity of the data w.r.t. [assumptions](http://varianceexplained.org/r/kmeans-free-lunch/) needed to use K-Means.
