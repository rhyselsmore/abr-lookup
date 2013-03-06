from flask import Flask, jsonify, render_template, abort, request, current_app
from suds.client import Client
from functools import wraps

app = Flask(__name__)
app.config.from_object('abr.settings')
app.debug = True
app.config.setdefault('ABR_GUID','None')

def requires_auth(f):
    """ Validates the API call """

    def check_auth(username,token):
        u = current_app.config.get('USERNAME')
        t = current_app.config.get('TOKEN')

        return username == u and token == t

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            abort(401)
        return f(*args, **kwargs)
    return decorated

def lookup(search):
    
    search = search.replace(' ','')

    d = {
        "successful" : False,
        "names" : [],
        "status" : "Not Found",
    }

    client = Client("http://abr.business.gov.au/abrxmlsearch/ABRXMLSearch.asmx?WSDL")

    request = client.factory.create(u'ABRSearchByABN')
    request.includeHistoricalDetails = 'n'
    request.authenticationGuid = app.config.get('ABR_GUID','None')
    request.searchString = search

    response = client.service.ABRSearchByABN(request).response

    if hasattr(response,'exception'):
        d['status'] = response.exception.exceptionDescription
        print response
        if response.exception.exceptionCode == "Search":
            status_code = 404
        else:
            status_code = 500
        resp = jsonify(**d)
        resp.status_code = status_code
        return resp

    if not hasattr(response,'businessEntity'):
        print response
        resp = jsonify(**d)
        resp.status_code = 404
        return resp

    entity = response.businessEntity

    if hasattr(entity,'legalName'):
        d["names"].append('%s %s' % (entity.legalName.givenName,entity.legalName.familyName))

    if hasattr(entity,'mainName'):
        d["names"].append('%s' % (entity.mainName.organisationName))

    if hasattr(entity,'mainTradingName'):
        for name in entity.mainTradingName:
            d["names"].append('%s' % (name.organisationName))

    if hasattr(entity,'otherTradingName'):
        for name in entity.otherTradingName:
            d["names"].append('%s' % (name.organisationName))
    
    d["status"] = entity.entityStatus[0].entityStatusCode
    d["successful"] = True

    return jsonify(**d)

@app.route('/api/lookup/<string:search>',methods=['GET'])
@requires_auth
def api_lookup(search):
    return lookup(search)

if __name__ == "__main__":
    app.run()