'''
Created on Apr 23, 2012

@author: jose
'''

import urllib, urllib2, base64

def name2phone(firstname, lastname):
    
    url = 'http://maltego-cloud.appspot.com/PersonToPhoneNumberArgentina'
    #url = 'http://127.0.0.1:8080/PersonToPhoneNumberArgentina'
    
    # Submit=BUSCAR&area=11&telefono=??????
    values = {'value' : '',
              'fields' : '',
             }

    values['value'] = base64.b64encode((firstname+' '+lastname).title())
    values['fields'] = base64.b64encode('firstname=%s#lastname=%s#' % (firstname,lastname))
    
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    #req.add_header('User-agent', 'Mozilla/5.0')
    cont = urllib2.urlopen(req).read()

    return cont

if __name__ == '__main__':
    
    print '#'*80
    print name2phone('juan','gomez')
    print '#'*80
    print name2phone('carla','lopez')
    print '#'*80
    print name2phone('maria','rampoldi')
    print '#'*80
    print name2phone('eduardo','chaves')
    print '#'*80
