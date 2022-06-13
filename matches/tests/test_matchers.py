import pytest

from matches.management.commands.match import TitleMatcher, SkillMatcher
from matches.models import Job, Candidate, Skill


class TestTitleMatcher:
    def test_matches_single_keyword(self):
        job = Job(title="senior python developer")
        candidate = Candidate(title="python")

        matcher = TitleMatcher()
        assert matcher.rank(job, candidate) == matcher.PERFECT_MATCH / 3


@pytest.mark.django_db
class TestSkillMatcher:
    def test_single_skill_is_a_perfect_match(self):
        skill = Skill.objects.create(name="c++")
        job = Job(skill=skill)
        candidate = Candidate.objects.create()
        candidate.skills.add(skill)

        matcher = SkillMatcher()
        assert matcher.rank(job, candidate) == matcher.PERFECT_MATCH
