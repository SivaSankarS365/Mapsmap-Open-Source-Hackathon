# Mapsmap Open Source Hackathon

## Introduction

> ### "Build an app for open source collaboration on maps of problems through crowdsourcing and crowdfunding"

The main objective of this hackathon is to develop a website app that organises modern civilisation problems in an intuitive manner. The idea is to create a platform to organise, manage and find fundings for civilisation problems like solving the issue of global warming to exploring the cosmos.


## Our Approach


 * All the problems in the site are assigned tags by a Smart AI system. 
 * When the user enters the site, a graph showing all available tags with interconnections between them is displayed.
 ![Sample Graph](https://user-images.githubusercontent.com/76562393/163673121-9ba31352-a6b6-402c-8f34-9ad45f294db5.jpeg)

 * The user can easily navigate to problems in his domain and also visualise the interconnections through the graph.
 * Once the user click a problem he will be navigated to the problem page where the user can view other users who are working on this, join the community working on the problem, provide funding, etc.
 * The funding system is managed through blockchain where user can invest in the problem.
 * User can also post a new problem in the network. An AI based system will automatically assign tags for the question.


 ## My contribution for the project

| Question     | Predictions|
| ----------- | ----------- |
|Is happiness just chemicals flowing through your brain or something more?     | psychology, biochemistry, biology, humans, brain      |
| Is there inherent order in nature or is it all chaos and chance?  | society, biology, evolution       |
| What is the meaning of a good life? |psychology, society, law, ethics, culture|



 

 * Built a smart AI system that can assign tags automatically once user enters a new problem. Tags can be added or removed from tagger system.
 * Developed algorithm to automatically organise the tags generated through graphs.
 ## Technical Details on my part
 * I collected all the questions and tags from [WorldBuilding](https://worldbuilding.stackexchange.com/), [The great outdoors](https://outdoors.stackexchange.com/), [Sustainable Living](https://sustainability.stackexchange.com/), [Space exploration](https://space.stackexchange.com/) stack exchange websites.
 * A fine tuned BERT based model is build from the collected data consisting of about 570 tags and 75,000 questions for training.
 * The model predicted with 99.65% binary accuracy on validation data.
 * An auxiliary model based on similarity scores was also build to deal with dynamic nature of the tags. (Tags can be removed or added by admin). 
 * The auxiliary model extracts all nouns (monograms and bigrams) from questions and embed them using Sense2Vec embeddings. A similarity search on the newly added tags is done to make prediction.
 * Once the websites gathers enough data, the BERT based model can be retrained on the collected data and thus the AI model will improve with time.
 * I also built a database to manage the tags. Tags are categorised into three types:
	 * White tags: 
		 * This are the tags that the BERT based model is trained on.
	 * Black tags: 
		 * This are the tags that should be removed from White tags. (Simulating deletion of tags)
	 * Blue tags: 
		 * This are newly assigned tags that are not yet incorporated into the BERT model. Auxiliary model is used to make prediction for this tags.
 * The assigned tags are graphed using the [ConceptNet](https://conceptnet.io/) database. 
---
 ## Note:
* Due to storage constraints in github all the data files that are larger than 500 MB are removed.
* This files includes:
	* Conceptnet database used for making graphs
	* BERT base model downloaded from tfhub
	* Preprocessing model for BERT downloaded from tfhub
	* model.h5, the trained weights.
	* Sense2Vec embeddings used for auxiliary model.
* [Link to google drive containing full files with all the data.](https://drive.google.com/drive/folders/1ADNcsjubNEMmTAziCumB7cuat1MobSXz?usp=sharing)
