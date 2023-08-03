# About this project
This project is an attempt to improve my understanding of vector-based retrieval and semantic modelling of text via very simple examples.

## Pre-requisites
To run this project you need:
1. Some familiarity with [Jupyter notebooks](https://jupyter.org/) and the [Python programming language](https://www.python.org/)
2. Access to a [MongoDB Atlas cluster](https://www.mongodb.com/atlas/database)

## Data
I used data from these sources for my examples:
* [Average body and brain weights for animals](https://www.open.edu/openlearn/science-maths-technology/mathematics-statistics/exploring-data-graphs-and-numerical-summaries/content-section-2.6#tbl001_006) from OpenLearn
* ['Home Education' by Charlotte M. Mason](https://www.gutenberg.org/cache/epub/71087/pg71087.txt)

## Usage
### Connect to Atlas
To use the notebook you will need to set up a `.env` file in this directory to store the connection URL for your Atlas cluster in the `MDB_URI` variable.
E.g. `MDB_URI="mongodb+srv://<user>:<password>@<cluster id>.mongodb.net/<database>"`

Read [this tutorial](https://www.mongodb.com/docs/atlas/tutorial/connect-to-your-cluster/) for more information about connecting to MongoDB Atlas.

### Create Atlas Search Index
[Create a new search index](https://www.mongodb.com/docs/atlas/atlas-search/create-index/) on your database using the JSON editor and the [index definition](/definition.json) included in this project.
