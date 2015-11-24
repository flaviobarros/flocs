from django.db import models
from django.contrib.auth.models import User
from tasks.models import TaskModel
from practice.models import TaskInstanceModel

class StudentTaskInfoModel(models.Model):
    """
    Persistent information about a student-task pair
    """

    student = models.ForeignKey(User)
    task = models.ForeignKey(TaskModel)

    class Meta:
        unique_together = ('student', 'task')
        index_together = ['student', 'task']

    # last instance of the task attempted by the user (not necessarily solved)
    last_instance = models.ForeignKey(TaskInstanceModel,
            null=True, default=None)

    def __str__(self):
        templ = 'student={student}, task={task}, last_instance={last_instance}'
        return templ.format(
            student=self.student.pk,
            task=self.task.pk,
            last_instance=self.last_instance.pk if self.last_instance else None
        )
