# Mapsmap Open Source Hackathon

## Overview

### "Create an app for open-source collaboration on problem maps through crowdsourcing and crowdfunding."

The goal of this hackathon is to build a web app that intuitively organizes modern civilization's challenges. The platform will enable users to catalog, manage, and fund solutions to global issues, from combating climate change to exploring the cosmos.

## Our Approach

* **Smart AI Tagging:** Problems on the site are automatically tagged by an AI system.
* **Interactive Graph Visualization:** Upon entering the site, users are greeted with a graph displaying all available tags and their interconnections.

 ![Sample Graph](https://user-images.githubusercontent.com/76562393/165536063-59029937-d666-428f-b282-9f071dca72ff.png)

* **User Navigation:** Users can explore problems within their domain and visualize connections through the graph.
* **Problem Engagement:** Clicking on a problem navigates the user to a dedicated page where they can join the community, contribute funding via blockchain, and engage with others working on the issue.
* **AI-Assisted Problem Posting:** Users can submit new problems, with the AI automatically assigning relevant tags.

## My Contributions

| Question     | Predicted Tags |
|--------------|----------------|
|Is happiness just chemicals flowing through your brain or something more? | psychology, biochemistry, biology, humans, brain |
|Is there inherent order in nature, or is it all chaos and chance? | society, biology, evolution |
|What is the meaning of a good life? | psychology, society, law, ethics, culture |

* **Smart AI Tagging System:** Developed an AI system that automatically assigns tags when a new problem is posted. Tags can be added or removed dynamically.
* **Graph Organization Algorithm:** Created an algorithm to automatically organize the generated tags into a graph.

## Technical Details

* **Data Collection:** Gathered questions and tags from various Stack Exchange sites, including [WorldBuilding](https://worldbuilding.stackexchange.com/), [The Great Outdoors](https://outdoors.stackexchange.com/), [Sustainable Living](https://sustainability.stackexchange.com/), and [Space Exploration](https://space.stackexchange.com/).
* **Model Development:** Fine-tuned a BERT-based model using the collected data, which included approximately 570 tags and 75,000 questions for training. The model achieved 99.65% binary accuracy on validation data.
* **Auxiliary Model:** Developed a supplementary model based on similarity scores to handle dynamic tag management (i.e., tags that can be added or removed by the admin). This model extracts nouns from questions, embeds them using Sense2Vec, and performs similarity searches to predict tags.
* **Continuous Improvement:** As the website gathers more data, the BERT model can be retrained, enhancing the AI's performance over time.
* **Tag Management Database:** Built a database to categorize tags into three types:
	* **White Tags:** Tags the BERT model is trained on.
	* **Black Tags:** Tags that are excluded from the White Tags (simulating tag deletion).
	* **Blue Tags:** Newly added tags not yet incorporated into the BERT model. The auxiliary model handles predictions for these tags.
* **Graph Visualization:** Used the [ConceptNet](https://conceptnet.io/) database to visualize the assigned tags.

---

## Note:
* Due to GitHub storage constraints, data files larger than 500 MB have been removed. This includes:
	* The ConceptNet database used for graph generation
	* BERT base model and preprocessing model from TensorFlow Hub
	* `model.h5` with trained weights
	* Sense2Vec embeddings used in the auxiliary model
* [Access the complete files and data on Google Drive.](https://drive.google.com/drive/folders/1ADNcsjubNEMmTAziCumB7cuat1MobSXz?usp=sharing)

---
