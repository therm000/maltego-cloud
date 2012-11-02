'''
Created on May 2, 2012

@author: jose
'''
import unittest, urllib, urllib2, base64


class TestRemote(unittest.TestCase):

    __server = ''

    def testPersonToPhoneNumberArgentina(self):
        
        url = 'http://maltego-cloud.appspot.com/PersonToPhoneNumberArgentina'
        #url = 'http://127.0.0.1:8080/PersonToPhoneNumberArgentina'
        
        # Submit=BUSCAR&area=11&telefono=?????
        values = {'value' : '',
                  'fields' : '',
                 }
    
        firstname = 'Carla'
        lastname = 'Lopez'
    
        values['value'] = base64.b64encode((firstname+' '+lastname).title())
        values['fields'] = base64.b64encode('firstname=%s#lastname=%s#' % (firstname,lastname))
        
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        
        cont = urllib2.urlopen(req).read()
    
        self.assertEqual(cont, 'NADA')
    
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()