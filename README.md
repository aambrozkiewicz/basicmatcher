# Quickstart

In order to run it, please make sure to [install poetry](https://python-poetry.org/docs/) first.

```shell
# Install all dependencies and setup a virtual env
poetry install
# Spawn shell that uses the created env
poetry shell
# Run migrations (sqlite by default)
./manage.py migrate
# Create superuser to access Django admin
./manage.py createsuperuser
# Start Django server
./manage.py runserver 8181
```

Go to http://127.0.0.1:8181/admin/

# Matcher CLI utility

To perform matches, please add some models using the admin panel first.

In order to run matching use command line utility, provide `JobID` as an argument, 
to which you are looking for Candidates.

```shell
./manage.py match <JobID>
```

Example run:
```
❯ ./manage.py match 1
Matching for Job Senior C++ Developer
senior c++ developer: 2.0
C++ Developer: 1.6666666666666665
Office manager: 0
```

Candidates are given with a rank which indicate their fit for the Job.
Results are sorted and one on top is the best fitting Candidate.


## Implementation details

`Matcher` is a class that describes a recipe on how to match characteristics of a Candidate to a given Job.

Each implementation of the `match` method should alter `rank` value between 1 and 0, where 1 means a perfect fit based on the given matcher.

```python
class Matcher:
    PERFECT_MATCH = 1

    def match(self, job, candidates):
        pass
```

`CandidateFinder` should be instanced with a list of Matchers we would like to use to perform the match.
This should help when adding another Matchers in the future.

```python
from matches.management.commands.match import CandidateFinder, TitleMatcher, SkillMatcher

CandidateFinder([TitleMatcher(), SkillMatcher()])
```