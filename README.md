# Analysis of FRONTEX Risk Analysis Reports

This project was conducted as an Exam for the course The Politics of Borders and Migration Control: Critical Social Science Approaches at the University of Copenhagen in Spring 2024 (https://kurser.ku.dk/course/astk18441u/2023-2024). The exam was graded 12 (A).

It showcases, how basic and computationally efficient NLP methods can support, up-scale and focus the analysis on a political text corpus.

# Project Overview

After giving an overview on the relevant political theory and existing research the project:

- scrapes Frontex' online archive and downloads the risk analysis reports as pdf files using **selenium**
- converts the pdf files to useable formats
- performs different computationally efficient NLP methods to analyze the text corpus, such as
	- word cloud
	- bi-grams using **nltk**
	- **Word2Vec** (with gensim)
	- TF-IDF using **sklearn**
- explores and visualizes the results in **seaborn and matplotlib**
