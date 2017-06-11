class player(object):
    """description of class"""
    def __init__(self):
        self.name = 'Dan Piao'
        self.email = 'dpiao@gentax.com'
        self.coach = True
        self.mu = 25.000
        self.sigma = 8.333

class match_doc(object):
    """ Model class for the pong object. We're storing this object into the database """
    def __init__(self):
        winner = 'Winner'
        loser = 'Loser'
        win_score = 11
        los_score = 0