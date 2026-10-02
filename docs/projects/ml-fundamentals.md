# Machine-learning fundamentals notebooks

[Repository](https://github.com/jeet-biswas/python) |
[Reviewed Perceptron notebook](https://github.com/jeet-biswas/python/blob/27578b5fdf0523ddfe7946e3de1fb81806512a8d/perceptron.ipynb)

The Perceptron exercise uses scikit-learn with CGPA and resume-score features to
explore a placement-label classification example. It inspects learned coefficients
and the intercept, then plots decision regions to connect a model's parameters
with its predictions. Another notebook explores data with Pandas.

## Reading the experiment

1. Identify the input columns and target label.
2. Inspect the data before fitting the estimator.
3. Follow how coefficients and the intercept form a decision boundary.
4. Compare the plotted boundary with the observed points.

The reviewed notebook does not provide a held-out evaluation. A useful extension
would separate training and test observations before fitting, record dataset
provenance, and compare class-level errors against a simple baseline. A plot of
training points alone cannot establish performance on new examples.

## Connection to application work

These exercises build intuition for the evaluation questions that appear in
larger projects: what constitutes an example, where a label comes from, whether
the split is independent, and what a wrong prediction means for a user.

[Back to profile](../../README.md)
