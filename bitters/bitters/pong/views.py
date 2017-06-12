"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from pong import app
import forms
import config
import pydocumentdb.document_client as document_client
import requests


"""
HELPERS!
"""
def createDB(client, DB):    
    db = client.CreateDatabase({ 'id': DB})

def createCollection(client, db, collectionName):
    collection = client.CreateCollection(db['_self'],{ 'id': collectionName })


def setup_collection(CollectionName):
    # Set up the clients to query for actors in these collections. 
    client = document_client.DocumentClient(config.DOCUMENTDB_HOST, {'masterKey': config.DOCUMENTDB_KEY})

    #Try accesesing the database
    try:
        db = next((data for data in client.ReadDatabases() if data['id'] == config.PONG_DB))
    except: #DB doesn't exist
        createDB(client, config.PONG_DB)

    db = next((data for data in client.ReadDatabases() if data['id'] == config.PONG_DB)) 
    # Get the collection from the database. 
    try:
        coll = next((coll for coll in client.ReadCollections(db['_self']) if coll['id'] == CollectionName))    
    except:
        createCollection(client, db, CollectionName)

    #Set the current collection back to the one we just created
    coll = next((coll for coll in client.ReadCollections(db['_self']) if coll['id'] == CollectionName))    
    
    return client, coll

def del_entity(client, collection, id):
    del_doc_iter = client.QueryDocuments(collection['_self'], 'select * from c where c.id = @id', { 'id' : id }).fetch_next_block()
    del_doc_iter = client.QueryDocuments(collection['_self'], {
                'query': 'select * from c where c.id = @id',
                'parameters': [{ 'name':'@id', 'value': id} ] } ).fetch_next_block()
    del_doc_id = del_doc_iter.__iter__().next()['_self']            
    ##TODO: Figure out what to do when the entity doesn't exist
    client.DeleteDocument(del_doc_id)

def read_Documents(client, collection, num, order = None):
    iter = client.QueryDocuments(collection['_self'], 'select top ' + str(num) + ' * from c ' + str(order))
    return iter.fetch_next_block()

    
def get_collection_docs_pong(client, collection_name):
    db = next((data for data in client.ReadDatabases() if data['id'] == config.PONG_DB))
    coll = next((coll for coll in client.ReadCollections(db['_self']) if coll['id'] == collection_name))    
    return client.ReadDocuments(coll['_self']).__iter__()
    
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/players', methods=['GET', 'POST'])
@app.route('/signup', methods=['GET', 'POST'])
def players(): 
    from pong.gameConfig.pong_entity.entities import player 
    client, coll = setup_collection(config.PLAYERS)
    form = forms.PlayerSignup()
    
    if form.validate_on_submit():
        #form has been validated. We can try creating a new document now. 
        if form.del_entity.data == "Delete":
            del_entity(client, coll, form.name.data)            
            form.del_entity.data = ""
        else:            
            obj =  player()
            obj.name = form.name.data
            obj.id = form.name.data
            obj.email = form.email.data
            obj.coach = form.coach.data

            document = client.UpsertDocument(coll['_self'], obj.__dict__)

    #Get all documents and populate on the screen
    docs = client.ReadDocuments(coll['_self']).__iter__()    
    
    return render_template('signup.html', 
                            title = 'Sign up', 
                            entityName = 'player',
                            form = form, 
                            existings = docs,
                            year=datetime.now().year)

@app.route('/matches', methods=['GET', 'POST'])
def matches():
    from pong.gameConfig.pong_entity.entities import match_doc
    from pong.gameConfig.pong_controller.match_controller import match_controller
    client, coll = setup_collection(config.MATCHES)
    form = forms.MatchForm()

    all_players = get_collection_docs_pong(client, config.PLAYERS)
    form.winner.choices = [(g['id'], g['name']) for g in all_players]
    form.loser.choices = form.winner.choices

    if form.validate_on_submit():
        #Create a match controller
        m_c = match_controller()
        m_c.setup_match_from_form(form)
        obj = m_c.get_matchFormDoc()
        document = client.UpsertDocument(coll['_self'], obj.__dict__)
        
        #calculate new scores
        m_c.load_players_from_db()
        m_c.update_player_ratings()

    #Get all documents and populate on the screen
    docs = read_Documents(client, coll, 10, 'order by c._ts desc')
    
    return render_template('matches.html', 
                            title = 'Latest Matches', 
                            form = form, 
                            existings = docs,
                            year=datetime.now().year)



@app.route('/ranking', methods=['GET'])
def ranking():
    client, coll = setup_collection(config.PLAYERS)
    all_players = get_collection_docs_pong(client, config.PLAYERS)
    players = [(g['mu'], g['name']) for g in all_players]
    sorted_players = sorted(players, reverse=True ,key=lambda tup:tup[0] )

    return render_template('ranking.html', 
                            title = 'Current Rankings', 
                            ranking = sorted_players,
                            year=datetime.now().year)


@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    import pong.gameConfig.pong_controller.invite as inv
    inv.sendemail()

    return render_template(
        'schedule.html',
        title='Home Page',
        year=datetime.now().year,
    )
