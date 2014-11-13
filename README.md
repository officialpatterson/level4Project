#level4Project

The level4Project is called **Good Tweet, Bad Tweet**.

The project aims to create an application that will be able to classify a tweet about an entity into one of several reputation dimensions and allow the end-user of the system to view the data appropriately.

## Tweet Enrichment

A separaet piece of software performs the feed-enrichment aspect of the system. It's main aim is to classify text into a reputation dimension. Other enrichments occur such as sentiment analysis and topic modelling to a lesser extent.



**Classifying tweet into a reputation dimension.**

The software implements a Naive Bayes classifer provided by the NLTK framework. Firstly, a vector is built from each tweet using the presence of terms in a document as a feature. Then training and classification follows.

