class World:
  def __init__(self):
    self.who = []
    self.pop = 0
    self.hap = 0
  def info(self):
    print ('list of people:')
    for p in self.who:
      print (f'{p.name}')
    print (f'population: {self.pop}')
    print (f'total happiness: {self.hap}')