from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from Maltego import MaltegoTransform

import base64

from external import solve_persona_ar


class NothingPage(webapp.RequestHandler):
    
    
    def post(self):
        self.response.out.write( '' )
            
    def get(self):
        self.response.out.write( '' )


            
class SampleTransform(webapp.RequestHandler):
    
    
    def post(self):
        
        if 'value' in self.request.arguments():
        
            #value = base64.b64decode(self.request.get('value'))
        
            mt = MaltegoTransform()
            #new_ent = mt.addEntity("Phrase", value + '!!!')
        
            op = mt.returnOutputString()

            self.response.out.write( op )

            self.response.headers['Content-Type'] = "text/xml"

        else:

            self.response.out.write( "Sample Maltego Transform" )

            self.response.headers["Content-Type"] = "text/plain"
            
            
            
class PersonToPhoneNumberArgentina(webapp.RequestHandler):

    def get(self):
    
            self.response.out.write( "PersonToPhoneNumberArgentina Maltego Transform" )

            self.response.headers["Content-Type"] = "text/plain"
        
    
    def post(self):
        
        if 'value' in self.request.arguments():
        
            #value = base64.b64decode(self.request.get('value'))

            fields = base64.b64decode(self.request.get('fields'))
            fields = fields.split('#')
            fs = {}
            for f in fields:
                if f.strip() != '':
                    field,f_value = tuple(f.split('='))
                    fs[field] = f_value
        
            mt = MaltegoTransform()
            
            #surname = value.split()[-1]
            #first_name = value.split()[0]
            #t = solve_persona_ar( ['persona_ar','telefono',surname+' '+first_name] )
            

            
            t = solve_persona_ar( ['persona_ar','telefono',fs['lastname']+' '+fs['firstname'] ] )

            for solution in t:
            
                new_ent = mt.addEntity("PhoneNumber", '54 ' + solution[-1].replace('(','').replace(')','').replace('-',' ') )
                
                phone = solution[-1].replace('(','').replace(')','').replace('-',' ')
                country = '54'
                city = phone.split()[0]
                area = phone.split()[1]
                last_digits = phone.split()[2]
                
                new_ent.addAdditionalFields(displayName='Country Code',fieldName='countrycode',value=country,matchingRule='strict')
                new_ent.addAdditionalFields(displayName='City Code',fieldName='citycode',value=city,matchingRule='strict')
                new_ent.addAdditionalFields(displayName='Area Code',fieldName='areacode',value=area,matchingRule='strict')
                new_ent.addAdditionalFields(displayName='Last Digits',fieldName='lastnumbers',value=last_digits,matchingRule='strict')
                new_ent.addAdditionalFields(displayName='PhoneType',fieldName='type',value='landline',matchingRule='strict')
        
        
            op = mt.returnOutputString()

            self.response.out.write( op )

            self.response.headers['Content-Type'] = "text/xml"

        else:


            self.response.out.write( "PersonToPhoneNumberArgentina Maltego Transform" )

            self.response.headers["Content-Type"] = "text/plain"
            
            

application = webapp.WSGIApplication([
                                      ('/SampleTransform', SampleTransform),
                                      ('/PersonToPhoneNumberArgentina', PersonToPhoneNumberArgentina),
                                      ('/', NothingPage),
                                      
                                      ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
