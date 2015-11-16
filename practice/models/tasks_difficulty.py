from django.db import models
from common.flow_factors import FlowFactor
from tasks.models import TaskModel

# weight (discriminacy) of a single concept in a task
CONCEPT_WEIGHT = 0.2

class TasksDifficultyModel(models.Model):
    """Model for a task's difficulty

       For every concept there is a boolean value, where true means that
       the task requires some knowledge of the specified concept.
       The first value is decimal number and represents general difficulty of
       the task.
    """

    # task to refer
    task = models.OneToOneField(TaskModel, primary_key=True)

    # programming concept difficulty
    programming = models.DecimalField(max_digits=4, decimal_places=3, verbose_name="General difficulty of the task")

    # conditions concept difficulty
    conditions = models.BooleanField(verbose_name="Difficulty of the conditions concept in the task")

    # loops concept difficulty
    loops = models.BooleanField(verbose_name="Difficulty of the loops concept in the task")

    # logic expressions concept difficulty
    logic_expr = models.BooleanField(verbose_name="Difficulty of the logic expressions concept in the task")

    # colors concept difficulty
    colors = models.BooleanField(verbose_name="Difficulty of the colors concept in the task")

    # tokens concept difficulty
    tokens = models.BooleanField(verbose_name="Difficulty of the tokens concept in the task")

    # pits concept difficulty
    pits = models.BooleanField(verbose_name="Difficulty of the pits concept in the task")

    def get_difficulty_dict(self):
        """Return dictionary representation of the task difficulty.

        For each concept holds:
        CONCEPT_WEIGHT - the concept is related with the task
        0 - the concept is not related with the task
        """
        difficulty_dict = {
            FlowFactor.TASK_BIAS: float(self.programming),
            FlowFactor.LOOPS: _convert_boolean_to_concept_weight(self.loops),
            FlowFactor.CONDITIONS: _convert_boolean_to_concept_weight(self.conditions),
            FlowFactor.LOGIC_EXPR: _convert_boolean_to_concept_weight(self.logic_expr),
            FlowFactor.COLORS: _convert_boolean_to_concept_weight(self.colors),
            FlowFactor.TOKENS: _convert_boolean_to_concept_weight(self.tokens),
            FlowFactor.PITS: _convert_boolean_to_concept_weight(self.pits)
        }
        return difficulty_dict

    def number_of_concepts(self):
        num = 0
        if self.conditions:
            num += 1
        if self.loops:
            num += 1
        if self.logic_expr:
            num += 1
        if self.colors:
            num += 1
        if self.tokens:
            num += 1
        if self.pits:
            num += 1
        return num

    def __str__(self):
        return 'task={task}, difficulty={difficulty}'.format(
            task=self.task.pk,
            difficulty=self.get_difficulty_dict())

def _convert_boolean_to_concept_weight(boolean):
    return CONCEPT_WEIGHT if boolean else 0