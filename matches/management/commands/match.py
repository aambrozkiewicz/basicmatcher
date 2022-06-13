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
        candidates = [
            {
                "candidate": candidate,
                "rank": 0,
            }
            for candidate in candidates
        ]

        for matcher in self.matchers:
            for candidate in candidates:
                # Here we could validate that value is between PERFECT_MATCH and 0.
                # It would be a good idea to run each rank in a separate background tasks
                # as their implementation is somewhat independent.
                candidate["rank"] += matcher.rank(job, candidate["candidate"])

        return candidates


class Command(BaseCommand):
    help = "Finds the best match"

    def add_arguments(self, parser):
        parser.add_argument("job_id", help="Job ID")

    def handle(self, *args, **options):
        finder = CandidateFinder([TitleMatcher(), SkillMatcher()])
        job = Job.objects.get(pk=options["job_id"])
        self.stdout.write(f"Matching for Job {job.title}")

        matched_candidates = finder.find(
            job, Candidate.objects.all().prefetch_related("skills")
        )
        matched_candidates.sort(key=lambda c: c["rank"], reverse=True)

        for matched_candidate in matched_candidates:
            print(f"{matched_candidate['candidate']}: {matched_candidate['rank']}")
