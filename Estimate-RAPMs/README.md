# Estimating Regularized Adjusted Plus-Minus (RAPM)

### What was this take-home about?

This repo contains work for a take-home project performed for a research position for an unnamed NBA franchise.

The main goal for this project was to build a command-line tool to estimate RAPM, both offensive and defensive ratings. The [original paper](http://www.sloansportsconference.com/wp-content/uploads/2015/09/joeSillSloanSportsPaperWithLogo.pdf) describing this model was provided to help get started.

The tool I was asked to develop would write player-level offensive and defensive ratings to a CSV file via a Python script. It was to accept as arguments:

1. Location of input file (the file included here `rapm_data.csv`)
* This data had possession-level lineup and scoring. Offensive lineups are given in the column `ConcatLineup` while defensive lineups are given in `ConcatLineupOpp` with periods delimiting the individual players.
2. Location of the output file to which the tool would write.
3. Any other parameter specifications that I thought would be necessary/useful -- but to provide default values when needed.

The tool to be developed was to assume that any model implemented to estimate the offensive and defensive RAPM for each player was already validated, so no true machine learning modeling workflow was needed.

### About the Code

My version of this tool is found in the script `get_rapm_estimates.py`, which was developed and tested on a MacBook Pro running macOS High Sierra v10.13.1 and `Python 3.6.4` (with `pandas 0.22.0` and `scikit-learn 0.19.1`).

Within this script, offensive and defensive RAPM for players are estimated as coefficients of a Ridge Regression model in a modification of the model described in original Sloan as well as [here](https://squared2020.com/2017/09/18/deep-dive-on-regularized-adjusted-plus-minus-i-introductory-example/) and [here](http://www.82games.com/ilardi2.htm). This implementation assumes a validated model with an already pre-specified penalty term which the user can optionally define (default = 2000), and does not filter the original data by a minimum number of possessions (or minutes) nor incorporate weighting of past data.

### Using the Code
To run this script:
1. Save script to directory of your choice.
2. Navigate to directory containing the script in the command line interface of your choice.
3. Run the following command(s):

Terminal (Mac):
* `chmod +x get_rapm_estimates.py` so the script is executable
* `./get_rapm_estimates.py -i inputfilepath -o outputfilepath [-p penalty]`

Cmd (Windows):
* `get_rapm_estimates.py - i inputfilepath -o outputfilepath [-p penalty]`

Make sure to specify the (full) relative path of both the input file and output files — these are required. If you do specify a penalty value (it is optional), make sure to specify one value that can be coerced to a float value (e.g., a numeric or float).

An example (in Terminal) if the input file is rapm_data.csv and the output file is to be named rapm_estimates.csv and we specify a Ridge penalty of 1000:

`./get_rapm_estimates.py -i path/to/rapm_data.csv -o rapm_estimates.csv -p 1000`
