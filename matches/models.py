from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    title = models.CharField(max_length=500)

    # This field could live on its own as a table "CandidateSkill"
    # with possible additional fields like "seniority".
    skills = models.ManyToManyField(Skill, related_name="skills", blank=True)

    def __str__(self):
        return self.title


class Job(models.Model):
    title = models.CharField(max_length=500)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="jobs")

    def __str__(self):
        return self.title
