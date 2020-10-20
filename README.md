# Talent Snapshot: Keyword Extraction and Analysis
My first attempt at keyword extraction and analysis using Spacy, pandas and numpy libraries and [Xu Liang's implementation of TextRank!](https://towardsdatascience.com/textrank-for-keyword-extraction-by-python-c0bae21bcec0) which was a great help.

I split the project into two parts - extraction and analysis. The extraction part code can be found in *"keyword_extraction.py"* and the collected keywords in "Keywords.xlsx." The main idea in the extraction was to use the textrank algorithm to remove stopwords and identify keywords that could be later compared to roles of interest during the analysis. This procedure was used in all sections but the education section. For education keywords, I collected data on the different types of degrees and checked for keywords related to the collected data.

The analysis part code can be found in *"keyword_analysis.py"* and results in "Snapshot Figures and Analysis.xlsx." For analysis, I made use of Spacy's **most_similar** function while using the large model to compare the extracted keywords to a certain role of interest and gauge their similarity. If similar, the person was counted as holding that role within FORKAIA.

Below are the results I obtained: 

![](https://github.com/induhiu/NLP-Keyword-Extraction-and-Analysis---Forkaia-Talent-Showcase/blob/master/Talent%20Showcase%20visualization.jpg)
