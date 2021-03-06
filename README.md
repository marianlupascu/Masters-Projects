
# Masters-Projects

> This repository contains AI projects -- screenshots/gif & source.

Thesis - in progress...

## [Year 2](Year%202)
<details><summary><i>Information Retrieval and Text Mining</i> - Romanian Language Information Retrieval System</summary>


`Java + Lucene` The project revolves around two entities: 1.Indexer - the class that starts from a set of documents that it takes as a parameter in the main function (args [0]) and creates an "inverted index" that it saves in the folder ".\index". This class reads documents using the DocumentReader class (which uses Tika) and then saves them as txt documents (which contain exactly the same information) in a temporary folder based on which the "inverted index" is built, then the temporary folder is stressed and the information is saved to disk in "inverted index". And 2.Searcher - the class that starts from the “inverted index” created previously and from a search sting still called query. This class returns documents that are revealed for the search string based on a confidence score.
How to run the code:
1. Start a terminal in P1 then add the document indexing command
```
java -Dfile.encoding=UTF-8 -classpath ".\out\production\P1;.\dependencies\lucene-core-8.6.3.jar;.\dependencies\tika-app-1.24.1.jar;.\dependencies\pdfbox-app-2.0.21.jar;.\dependencies\lucene-queryparser-8.6.3.jar;.\dependencies\lucene-analyzers-common-8.6.3.jar" com.main.Indexer ".\docs"
```
2. After indexing you can search for various information with the command. The project was run with Java 15.
```
java -Dfile.encoding=UTF-8 -classpath ".\out\production\P1;.\dependencies\lucene-core-8.6.3.jar;.\dependencies\tika-app-1.24.1.jar;.\dependencies\pdfbox-app-2.0.21.jar;.\dependencies\lucene-queryparser-8.6.3.jar;.\dependencies\lucene-analyzers-common-8.6.3.jar" com.main.Searcher "to modify"
```
</details>

<details><summary><i>Information Retrieval and Text Mining</i> - 
Add Lyrics-Based Music Genre Classification</summary>

`Python` Music genre classification, especially using lyrics alone, remains a challenging topic in Music Information Retrieval. In this project I apply a several methods to classify a large dataset of intact song lyrics.

(Year%201/Syntactic%20Modeling%20of%20Biological%20Systems/Learning%20representations%20of%20microbe–metabolite/Peper_LM.pdf)
![sumary](https://github.com/marianlupascu/Masters-Projects/blob/master/Year%202/Information%20Retrieval%20and%20Text%20Mining/Lyrics-Based%20Music%20Genre%20Classification/sumary.PNG?raw=true)
</details>

<details><summary><i>Deep Learning</i> - Deep Hallucination Classification</summary>

`Python` Deep image hallucination classification challenge in which I train deep classification models on a data set containing images generated by deep generative models.
The analysis report and explanations can be found [here](https://github.com/marianlupascu/Masters-Projects/blob/master/Year%202/Deep%20Learning/Documentation.pdf)
![doc](https://github.com/marianlupascu/Masters-Projects/blob/master/Year%202/Deep%20Learning/2021-02-23%2011_16_58-Window.png?raw=true)
</details>

<details><summary><i>Natural language processing 2</i> - Fake News Detection</summary>

`Python` In our society, the spread of fake news is increasing drastically due to which people are believing in unreal incidents. So it is utmost necessary to differentiate the real news from the fake ones and present them to society.
The analysis report and explanations can be found [here](https://github.com/marianlupascu/Masters-Projects/blob/master/Year%202/Natural%20language%20processing%202/Fake-News-Detection.pdf)
![doc](https://github.com/marianlupascu/Masters-Projects/blob/master/Year%202/Natural%20language%20processing%202/2021-02-23%2011_22_27-Window.png?raw=true)
>Contributors:
>  * Zugravu Andrei
>  * Calinescu Valentin

</details>

<details><summary>Other Classes</summary>
  <li> Applied Cryptography </li>
</details>

## [Year 1](Bachelors%20Year%201)

- _Computer Vision_ – [Video analysis of a snooker footage](https://github.com/marianlupascu/Video-analysis-of-a-snooker-footage)
- _Computer Vision_ – [Automatic grading of multiple choice tests](https://github.com/marianlupascu/Automatic-grading-of-multiple-choice-tests)

<details><summary><i>Practical Machine Learning</i> - Classify gestures by reading muscle activity</summary>

`Python` A recording of human hand muscle activity producing four different hand gestures.
The analysis report and explanations can be found [here](Year%201/Practical%20Machine%20Learning/Classify%20gestures%20by%20reading%20muscle%20activity/DocEN.pdf)
![doc](Year%201/Practical%20Machine%20Learning/Classify%20gestures%20by%20reading%20muscle%20activity/2020-07-06%2020_31_24-Greenshot.png)
</details>

<details><summary><i>Practical Machine Learning</i> - Suicide Rates Overview 1985 to 2016</summary>

`Python` Suicide Rates Overview 1985 to 2016 Compares socio-economic info with suicide rates by year and country.
The analysis report and explanations can be found [here](Year%201/Practical%20Machine%20Learning/Suicide%20Rates%20Overview%201985%20to%202016/Report%20_%20P2.pdf)
![doc](Year%201/Practical%20Machine%20Learning/Suicide%20Rates%20Overview%201985%20to%202016/2020-07-06%2020_34_46-Greenshot.png)
</details>

<details><summary><i>Programming efficient algorithms</i> - On the Decision Tree Complexity of String Matching</summary>

A natural problem is to determine the number of characters that need to be queried (i.e. the decision tree complexity) in a string in order to decide whether this string contains a certain pattern. Rivest showed that for every pattern p, in the worst case any deterministic algorithm needs to query at least n − |p| + 1 characters, where n is the length of the string and |p| is the length of the pattern. 
The analysis report and explanations can be found [here](Year%201/Programming%20efficient%20algorithms/Complexitatea%20algoritmului%20de%20String%20Matching.pdf)
![doc](Year%201/Programming%20efficient%20algorithms/2020-07-06%2019_35_03-Greenshot.png)
</details>

<details><summary><i>Syntactic Modeling of Biological Systems</i> - Learning representations of microbe–metabolite</summary>

Metabolic-microbial relationships are essential for the study of the microbiome. A new method is introduced that has the power to analyze the metabolite-microbe relationships. This new method is based on a technology not used so far in the study of metabolized microbial interactions, namely machine learning.
It is proved by 5 experiments: two experiments on cystic pulmonary fibrosis, one on the wetting of the biocrust, in the analysis of the impact of a high fat diet in murine a bacterium responsible for the excess production of a new bile acid is determined and in the analysis of in ammatory bowel disease and the colon identify a bacterium responsible for this disease as it was not initially associated with this disease in the Human Microbiome Project, as this method of analyzing metabolite microbe interactions has higher performance than previous methods (which are purely statistical) to do this thing.

The analysis report and explanations can be found [here](Year%201/Syntactic%20Modeling%20of%20Biological%20Systems/Learning%20representations%20of%20microbe–metabolite/Peper_LM.pdf)
![doc](Year%201/Syntactic%20Modeling%20of%20Biological%20Systems/Learning%20representations%20of%20microbe–metabolite/2020-07-06%2019_37_08-Greenshot.png)
</details>

<details><summary>Other Classes</summary>
  <li> Advance Machine Learning </li>
  <li> Knowledge Representation and Reasoning </li>
  <li> Natural Language Processing </li>
  <li> Probabilistic programming </li>
</details>

<p  align="center">
<span>Lupascu Marian </span>  <img  src="https://github.com/marianlupascu/School-Projects/blob/master/Bachelors%20Year%202/Web%20Techniques/CSS%20Project/img/mini-logo.png?raw=true">
</p>
