from trueskill import Rating, quality_1vs1, rate_1vs1
from forms import MatchForm
from pong.gameConfig.pong_entity.entities import match_doc
import pydocumentdb.document_client as document_client
import config
class match_controller(object):    
    """object used to calculate pong class"""
    def __init__(self):
        """use global settings"""
        self.m_db = match_doc()
        self.win_doc, self.los_doc = None, None
        self.client = document_client.DocumentClient(config.DOCUMENTDB_HOST, {'masterKey': config.DOCUMENTDB_KEY})
        self.db = next((data for data in self.client.ReadDatabases() if data['id'] == config.PONG_DB))
        self.coll = next((coll for coll in self.client.ReadCollections(self.db['_self']) if coll['id'] == config.PLAYERS))

    #Players are tuples of mu, sigma
    def calc_player_ratings(self, winner, loser):
        r1,r2 = Rating(winner), Rating(loser)
        r3, r4 = rate_1vs1(r1, r2)
        return r3, r4

    def ratings(self):
        return self.r1, self.r2

    def load_players_from_db(self, winner=None, loser=None):
        winner =  self.m_db.winner  if winner is None else winner 
        loser =  self.m_db.loser if loser is None else loser        
        #def load_players_from_db(self, winner=self.m_db.winner, loser=self.m_db.loser):
        #Winner and Losers are just strings/name, this will load them as docs.              
        self.win_doc = next((doc for doc in self.client.ReadDocuments(self.coll['_self']) if doc['id'] == winner))
        self.los_doc = next((doc for doc in self.client.ReadDocuments(self.coll['_self']) if doc['id'] == loser))

    def update_player_ratings(self):
        win_rate, los_rate = self.calc_player_ratings((self.win_doc['mu'], self.win_doc['sigma']), (self.los_doc['mu'], self.los_doc['sigma']))
        self.win_doc['mu'], self.win_doc['sigma']= win_rate.mu, win_rate.sigma
        self.los_doc['mu'], self.los_doc['sigma']= los_rate.mu, los_rate.sigma
        self.client.UpsertDocument(self.coll['_self'], self.win_doc)
        self.client.UpsertDocument(self.coll['_self'], self.los_doc)

    def setup_match_from_form(self, form):
        self.m_db.winner = form.winner.data
        self.m_db.loser = form.loser.data
        self.m_db.win_score = form.win_score.data
        self.m_db.los_score = form.los_score.data        
        
    def get_matchFormDoc(self):
        return self.m_db