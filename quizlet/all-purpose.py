import pyquizlet

print 34


quizlet = pyquizlet.Quizlet('XXXX') 
s = quizlet.search_sets('Spanish') 
#s = quizlet.get_set('6009523', paged=False)

print s
