# Who Are Those Programmers? Part 1: On Competitiveness

A data-driven personality test (you could also call it a serious anthropological study) using data from Stack Overflow’s 2017 Developer Survey.

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [Results](#results)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>

Python 3.0 is required to run the code.

In addition, the following libraries are also required. 
- pandas
- scipy
- statsmodels
- matplotlib

## Project Motivation <a name="motivation"></a>

The 2017 Stack Overflow Developer Survery asked many interesting questions related to personality type. This project uses the responses from those survey questions with the goal of drawing some compelling (and hopefully not stereotypical) personality profiles of programmers, particularly professional developers based in the US.

This repo contains the part 1 of the project, which focuses on competitiveness. 

In particular, we're interested in a survey question that asked people whether they agree or disagree with the following statement:

*"I think of myself as competing with my peers"*


## File Descriptions <a name="files"></a>

This project includes one Jupyter notebook. 

- **Stackoverflow_PersonalitySurvey17.ipynb**: includes analysis and results with visualizations to answer the following questions - 
	- How did people answer the relevant survey questions?
	- Can we tell who the competitive programmers are?

The notebook imports modules from 4 `.py` files in the `Module` directory.

- **Utilities.py**: includes a function to plot categorical features
- **CleanDataFrame.py**: includes several functions for cleaning the data frame created during the project
- **InferentialStatistics.py**: includes several functions for performing statistical analysis, such as the chi-square test of independence and the one proportion z-test
- **CreateCompTable.py**: includes several functions for creating the final comparison tables with visualizations

## Results <a name="results"></a>

A Medium post with summarized findings can be found [here](....).

Give it a clap if you enjoyed reading it!

## Licensing, Authors, Acknowledgements <a name="licensing"></a>

You can find the licensing for the data and other descriptive information on [Kaggle](https://www.kaggle.com/stackoverflow/so-survey-2017/data).



