from flask import Flask, jsonify, render_template
from suds.client import Client

app = Flask(__name__)
app.config.from_object('abr.settings')
app.debug = True

def lookup(search):
    client = Client("http://abr.business.gov.au/abrxmlsearch/ABRXMLSearch.asmx?WSDL")
    request = client.factory.create(u'ABRSearchByABN')
    request.searchString = search
    request.includeHistoricalDetails = 'n'
    #request.authenticationGuid = ''
    print client.service.ABRSearchByABN(request)
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/lookup/<string:search>',methods=['GET'])
def api_lookup(search):
    return jsonify(**{})
