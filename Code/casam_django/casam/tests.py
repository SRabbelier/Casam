import unittest
from django.test import TestCase
from casam.models import Project
from uuid import UUID

class SimpleApplicationTestCase(unittest.TestCase):
    def testProjects(self):
        self.project1 = Project(name='Project1')
        
        #Make sure that the object was not yet added
        self.assertEquals(Project.objects.all().count(),0)
        self.project1.save()
        
        self.project2 = Project(name='Project 2')
        #Although a second object has been created, it should not have been added
        self.assertEquals(Project.objects.all().count(),1)
        self.project2.save()
        
        #The saving of Project 2 should make a total count of 2 projects
        self.assertEquals(Project.objects.all().count(),2)
        
        #Assure that the id's of the 2 projects are not the same
        self.assertNotEquals(self.project1.id.hex,self.project2.id.hex)
        
        #Project 1 should be added before Project 2
        self.assertTrue(self.project1.added < self.project2.added)
    
        #DELETING FAILS
        #oldid = self.project1.id
        #after deleting Project 1, the counter should be back to 1
        #self.project1.clear()
        #Project.objects.all().delete()
        #self.assertEquals(Project.objects.all().count(),1)
        #Project.objects.get(id = oldid).entry_set.remove()
        #p1 = Project.objects.get(id = oldid)
        #print p1
        
        #Project.objects.all().remove()
        
    #def tearDown(self):
    #    allProjects = Project.objects.all()
    #    for p in allProjects:
    #        p.delete()
            
