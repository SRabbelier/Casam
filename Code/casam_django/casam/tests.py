import unittest
from casam.models import Project

class SimpleApplicationTestcase(unittest.TestCase):
    def testProjects(self):
        self.project1 = Project(name='Project1')
        self.assertEquals(Project.objects.all().count(),0)
        self.project1.save()
        self.project2 = Project(name='Project 2')
        self.assertEquals(Project.objects.all().count(),1)
        self.project2.save()
        self.assertEquals(Project.objects.all().count(),2)
        self.assertNotEquals(self.project1.id,self.project2.id)
