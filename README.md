This small script is made to retrieve the most popular recent GitHub repos that have one or more of the following topics:

* `deep-learning`
* `machine-learning`
* `deep-neural-networks`
* `ml`
* `deep-neural-networks`

To use this, setup your GitHub API following [these instructions](https://docs.github.com/en/rest/quickstart?apiVersion=2022-11-28). 

To use:

```
git clone git@github.com:Zettablock/github-project-scraper.git
cd github-project-scraper
python main.py --weeks 12
```

The output will be in a json called `deep_learning_repos.json`. 

