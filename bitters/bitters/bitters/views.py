"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from bitters import app
from forms import VoteForm
import forms
import config
#from webapp.gameConfig.entity import placeable_entitity
import pydocumentdb.document_client as document_client


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

@app.route('/create')
def create():
    """Renders the contact page."""
    client = document_client.DocumentClient(config.DOCUMENTDB_HOST, {'masterKey': config.DOCUMENTDB_KEY})

    # Attempt to delete the database.  This allows this to be used to recreate as well as create
    try:
        dbs = client.ReadDatabases()
        db = next((data for data in client.ReadDatabases() if data['id'] == config.DOCUMENTDB_DATABASE))
        client.DeleteDatabase(db['_self'])
    except:
        pass

    # Create database
    db = client.CreateDatabase({ 'id': config.DOCUMENTDB_DATABASE })

    # Create collection
    collection = client.CreateCollection(db['_self'],{ 'id': config.DOCUMENTDB_COLLECTION })

    # Create document
    document = client.CreateDocument(collection['_self'],
        { 'id': config.DOCUMENTDB_DOCUMENT,
          'Web Site': 0,
          'Cloud Service': 0,
          'Virtual Machine': 0,
          'name': config.DOCUMENTDB_DOCUMENT 
        })

    return render_template(
       'create.html',
        title='Create Page',
        year=datetime.now().year,
        message='You just created a new database, collection, and document.  Your old votes have been deleted')

@app.route('/vote', methods=['GET', 'POST'])
def vote(): 
    form = VoteForm()
    replaced_document ={}
    if form.validate_on_submit(): # is user submitted vote  
        client = document_client.DocumentClient(config.DOCUMENTDB_HOST, {'masterKey': config.DOCUMENTDB_KEY})

        # Read databases and take first since id should not be duplicated.
        db = next((data for data in client.ReadDatabases() if data['id'] == config.DOCUMENTDB_DATABASE))

        # Read collections and take first since id should not be duplicated.
        coll = next((coll for coll in client.ReadCollections(db['_self']) if coll['id'] == config.DOCUMENTDB_COLLECTION))

        # Read documents and take first since id should not be duplicated.
        doc = next((doc for doc in client.ReadDocuments(coll['_self']) if doc['id'] == config.DOCUMENTDB_DOCUMENT))

        # Take the data from the deploy_preference and increment our database
        doc[form.deploy_preference.data] = doc[form.deploy_preference.data] + 1
        doc[form.deploy_preference2.data] = doc[form.deploy_preference2.data] + 1
        replaced_document = client.ReplaceDocument(doc['_self'], doc)

        # Create a model to pass to results.html
        class VoteObject:
            choices = dict()
            total_votes = 0

        vote_object = VoteObject()
        vote_object.choices = {
            "Web Site" : doc['Web Site'],
            "Cloud Service" : doc['Cloud Service'],
            "Virtual Machine" : doc['Virtual Machine']
        }
        vote_object.total_votes = sum(vote_object.choices.values())

        return render_template(
            'results.html', 
            year=datetime.now().year, 
            vote_object = vote_object)

    else :
        return render_template(
            'vote.html', 
            title = 'Vote',
            year=datetime.now().year,
            form = form)


@app.route('/actors', methods=['GET', 'POST'])
def viewactors(): 
    default_actors = ['blacksmith', 'butler', 'area_boss', 'king', 'area_minion1', 'area_minion2', 'area_minion3', 'merchant']
    
    # Set up the clients to query for actors in these collections. 
    client = document_client.DocumentClient(config.DOCUMENTDB_HOST, {'masterKey': config.DOCUMENTDB_KEY})
    # Read databases and take first since id should not be duplicated.
    db = next((data for data in client.ReadDatabases() if data['id'] == config.DOCUMENTDB_DATABASE))

    # Read collections and take first since id should not be duplicated.
    coll = next((coll for coll in client.ReadCollections(db['_self']) if coll['id'] == config.DOCUMENTDB_COLLECTION))

    # Read documents and take first since id should not be duplicated.
    doc = next((doc for doc in client.ReadDocuments(coll['_self']) if doc['id'] == config.DOCUMENTDB_DOCUMENT))


@app.route('/placeable', methods=['GET', 'POST'])
def placeable():  
    from bitters.gameConfig.entity.placeable_entity import placeableType
    # Set up the clients to query for actors in these collections. 
    client = document_client.DocumentClient(config.DOCUMENTDB_HOST, {'masterKey': config.DOCUMENTDB_KEY})
    form = forms.PlaceableForm()

    #Try accesesing the database
    try:
        db = next((data for data in client.ReadDatabases() if data['id'] == config.BITTERS_CONFIG))
    except: #DB doesn't exist
        createDB(client, config.BITTERS_CONFIG)
    
    # Get the collection from the database. 
    try:
        coll = next((coll for coll in client.ReadCollections(db['_self']) if coll['id'] == config.PLACEABLES))    
    except:
        createCollection(client, db, config.PLACEABLES)

    if form.validate_on_submit():
        #form has been validated. We can try creating a new document now. 
        #TODO: Check for the ID/name to see if it exists first before submitting. Otherwise gonna throw error. 
        placeable_object =  placeableType()
        placeable_object.name = form.placeableName.data
        placeable_object.id = form.placeableName.data
        placeable_object.description = form.description.data

        document = client.CreateDocument(coll['_self'], placeable_object.__dict__)
    #TODO: Populate all the existing placeables

    #Grab the first one for now. See about it later
    docs = client.ReadDocuments(coll['_self'])
    sampleDoc = docs.__iter__().next()
    
    return render_template('placeable.html', 
                            title = 'Placeables', 
                            form = form, 
                            existing = sampleDoc,
                            year=datetime.now().year)


def createDB(client, DB):    
    db = client.CreateDatabase({ 'id': DB})

def createCollection(client, db, collectionName):
    collection = client.CreateCollection(db['_self'],{ 'id': collectionName })