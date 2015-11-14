from django.db import models
from django.contrib.auth.models import User

from decimal import Decimal


class StudentsSkillModel(models.Model):
    """Model for a student skill matrix

       For every concept there is number between -1 and 1 representing skill in
       certain concept.
    """

    # init values
    PROGRAMMING = Decimal(-1)
    CONCEPTS    = Decimal(-1)
    
    # student to refer with foreign key
    student = models.OneToOneField(User, primary_key=True)

    # programming concept difficulty
    programming = models.DecimalField(max_digits=4, decimal_places=3, default=PROGRAMMING, verbose_name="General skill")

    # conditions concept difficulty
    conditions = models.DecimalField(max_digits=4, decimal_places=3, default=CONCEPTS, verbose_name="Skill in conditions concept")

    # loops concept difficulty
    loops = models.DecimalField(max_digits=4, decimal_places=3, default=CONCEPTS, verbose_name="Skill in loops concept")

    # logic expressions concept difficulty
    logic_expr = models.DecimalField(max_digits=4, decimal_places=3, default=CONCEPTS, verbose_name="Skill in logic expressions concept")

    # colors concept difficulty
    colors = models.DecimalField(max_digits=4, decimal_places=3, default=CONCEPTS, verbose_name="Skill in colors concept")

    # tokens concept difficulty
    tokens = models.DecimalField(max_digits=4, decimal_places=3, default=CONCEPTS, verbose_name="Skill in tokens concept")

    # pits concept difficulty
    pits = models.DecimalField(max_digits=4, decimal_places=3, default=CONCEPTS, verbose_name="Skill in pits concept")

    def to_vector(self):
       """Return vector representation of the task difficulty.
          For each concept holds: 
           1 - the concept is related with the task
          -1 - the concept is not related with the task
       """
       return [self.programming,
               self.conditions,
               self.loops,
               self.logic_expr,
               self.colors,
               self.tokens,
               self.pits
               ]
