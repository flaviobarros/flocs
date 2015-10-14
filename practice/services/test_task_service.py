"""Unit test of task service
"""

from django.test import TestCase
from practice.models import TaskModel
from . import task_service


class TaskServiceTest(TestCase):

    def test_get_next_task(self):
        stored_task = TaskModel.objects.create(maze_settings="{}",
                workspace_settings='{"foo": "bar"}')
        retrieved_task = task_service.get_next_task()
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(stored_task.to_json(), retrieved_task)

    def test_no_task_available(self):
        # if there are no tasks available, task_servise should raise
        # LookupError
        self.assertRaises(LookupError, task_service.get_next_task)