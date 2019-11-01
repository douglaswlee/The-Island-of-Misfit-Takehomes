# Concrete Strength Prediction -- May 2019

### What is this?

This repo contains work for a take-home assignment for the NYC Department of Education (I am posting the exact name of the potential employer since part of this assigmment required posting it in a public Github repo). This assignment was the stage of the interview process following an initial phone screen. From completion of this assignment, I progressed to an on-site interview, and my status is still to be determined.

### What was this take-home about?

For this assignment, I was asked to download the [Concrete Slump Test Data Set](https://archive.ics.uci.edu/ml/datasets/Concrete+Slump+Test) from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php) and answer a series of questions that are included in the notebook **Concrete_Strength_Prediction.ipynb**.

### How long did you have to do this assignment?

24 hours.

### Additional Notes

* For the EDA section, I probably could have checked the data types and dug a little deeper to check for null values.

* For the correlation section, I am still not entirely certain what was to be achieved with binning the data or what a more intelligent version of this analysis should look like. I was hesitant to use any kind of "traditional" correlation analysis since the standard (Pearson) correlation coefficient is a [measure of linear association](https://www.bmj.com/about-bmj/resources-readers/publications/statistics-square-one/11-correlation-and-regression) and the data and analysis were clearly not geared towards linear regression.

* In both modeling sections, I ought to have been more systematic in determining the range of the hyperparameters to evaluate over (maybe by fitting without anything more than the defaults to get some bounds on the hyperparameters). I also should have briefly commented on whether ther was any over/underfitting for at least the Decision Tree Regression portion. For the Random Forest Regression, I believe I should have been doing feature selection before any modeling (cross-validating with `sklearn.feature_selection.SelectFromModel`). I also basically ignored the request for visualizaiton (which is not really possible, but I needed to be explicit in explaining that).
