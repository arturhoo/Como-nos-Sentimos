from beanstalkc import Connection


c = Connection()
stats = c.stats()
jobs = stats['current-jobs-ready']
print jobs
