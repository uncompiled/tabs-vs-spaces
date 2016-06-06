# Tabs vs Spaces

... because [Silicon Valley](http://www.popsci.com/inside-silicon-valleys-spaces-and-tabs-debate)

This repo consists of scripts and data pulled from top repos starred on 
GitHub as an attempt to find out what open source contributors tend to prefer.

## Usage

**Files**

- `data/` contains some output from the last time this was run.
- `scripts/` contains some Python scripts that you can use to  query for repos from GitHub.

**Dependencies**

- [git](https://git-scm.com/) needs to be installed to fetch the repo (to minimize API calls)

**Environment Variables**

- `GITHUB_ACCESS_TOKEN` should contain your GitHub auth token so you don't get [rate limited](https://developer.github.com/v3/search/#rate-limit)

### Step-by-step

1. `export GITHUB_ACCESS_TOKEN=<your github token>` 
2. `python scripts/find_repos.py > data/top_repos.json`
3. `python scripts/process_repos.py data/top_repos.json data/tabs_vs_spaces.json`

## Credits

- `indent_finder.py` sourced from Steven Myint's [fork](https://github.com/myint/indent-finder/blob/master/plugin/indent_finder.py).
  It wasn't perfect, but it handled the majority of files. Should use the corpus of GitHub repos to fix edge cases and outliers.

## License

MIT