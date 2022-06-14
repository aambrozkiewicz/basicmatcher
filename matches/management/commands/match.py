import collections

from django.core.management.base import BaseCommand

from matches.models import Candidate, Job


class Matcher:
    PERFECT_MATCH = 1

    def rank(self, job, candidates):
        raise NotImplemented


class TitleMatcher(Matcher):
    @staticmethod
    def tokenize(keywords):
        return list(map(str.lower, keywords.split(" ")))

    def rank(self, job, candidate):
        keywords = self.tokenize(job.title)
        step = self.PERFECT_MATCH / len(keywords)
        return sum(
            [step if k in self.tokenize(candidate.title) else 0 for k in keywords]
        )


class SkillMatcher(Matcher):
    def rank(self, job, candidate):
        return self.PERFECT_MATCH if job.skill in candidate.skills.all() else 0


class CandidateFinder:
    def __init__(self, matchers: list[Matcher]):
        self.matchers = matchers

    def find(self, job, candidates):
        matches = collections.defaultdict(int)

        for matcher in self.matchers:
            for candidate in candidates:
                # Here we could validate that value is between PERFECT_MATCH and 0.
                # It would be a good idea to run each rank in a separate background tasks
                # as their implementation is somewhat independent.
                matches[candidate] += matcher.rank(job, candidate)

        return matches


class Command(BaseCommand):
    help = "Finds the best match"

    def add_arguments(self, parser):
        parser.add_argument("job_id", help="Job ID")

    def handle(self, *args, **options):
        finder = CandidateFinder([TitleMatcher(), SkillMatcher()])
        job = Job.objects.get(pk=options["job_id"])
        self.stdout.write(f"Matching for Job {self.style.SUCCESS(job.title)}")

        matches = finder.find(job, Candidate.objects.all().prefetch_related("skills"))
        sorted_matches = dict(
            sorted(matches.items(), key=lambda item: item[1], reverse=True)
        )

        for candidate, rank in sorted_matches.items():
            self.stdout.write(f"{candidate}: {self.style.WARNING(str(rank))}")
