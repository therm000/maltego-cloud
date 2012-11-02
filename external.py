#
#   Copyright 2009-2012 Jose Ignacio Orlicki, Some Rights Reserved.
#
#    This file is part of Tuplets.
#
#    Tuplets is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Tuplets is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Tuplets.  If not, see <http://www.gnu.org/licenses/>.
#
#    Questions, comments?  http://twitter.com/therm000 and similar gugle mail...
#

#!/usr/bin/python


import urllib, urllib2
import time, re

#import simplejson as json
#import twython
from BeautifulSoup import BeautifulSoup
#from tuplet import Tuplet

#from secret import Secrets

import mechanize

external_list = [
                   'twitter_mentions', 'tw_mentions',
                   'alpha',   
                   'socialgraph', 'sg',                                       
                   'facebook_user',  'fb_user',
                   'auto_ar', 'automotor_ar',
                   'telefono_ar', 'fono_ar',
                   'persona_ar', 'nombre_ar',
                ]

tuplet_class = None

def is_external(token):    
    return token in external_list


def process(t, limit=10):
    
    if t[0] == 'twitter_mentions' or t[0] == 'tw_mentions':
        ret_list = solve_twitter(t,limit)
    elif t[0] == 'alpha':
        ret_list = solve_alpha(t,limit)
    #elif t[0] == 'socialgraph' or t[0] == 'sg':
    #    ret_list = solve_socialgraph(t,limit)
    elif t[0] == 'facebook_user' or t[0] == 'fb_user':
        ret_list = solve_facebook(t,limit)
    elif t[0] == 'auto_ar' or t[0] == 'automotor_ar' :
        ret_list = solve_auto_ar(t,limit)
    elif t[0] == 'telefono_ar' or t[0] == 'fono_ar' :
        ret_list = solve_telefono_ar(t,limit)
    elif t[0] == 'persona_ar' or t[0] == 'nombre_ar' :
        ret_list = solve_persona_ar(t,limit)

    return ret_list


def sanitize(desc):
    desc = desc.replace('"','\'')
    desc = desc.replace(u'\xe1',u'a').replace(u'\xe9',u'e').replace(u'\xed',u'i').replace(u'\xf3',u'o').replace(u'\xfa',u'u')
    return ''.join([c for c in desc if ord(c) < 128])



# http://breakingcode.wordpress.com/
#def solve_socialgraph(t, limit=10):
#
#        if len(t) < 2 or (len(t) == 2 and t[1].isupper()) or len(t) > 3:
#            return []
#
#        ret_list = []
#        if t[1].islower():# and t[2][0].isupper():
#            sg_key = 'nodes_referenced'
#            input_data = t[1]                
#        elif t[1][0].isupper() and t[2].islower():
#            #nodes_referenced_by
#            sg_key = 'nodes_referenced_by'
#            input_data = t[2]
#        
#        enc_input = urllib.urlencode({'bla':input_data}).split('=')[1]
#        base_url = 'http://socialgraph.apis.google.com/lookup?q=%s&fme=1&edi=1&edo=1&pretty=1&callback='
#        url = base_url % enc_input
#        #try:
#        cont = urllib2.urlopen(url).read()
#        obj = json.loads( cont )
#        
#        canonical_input = obj['canonical_mapping'][input_data]            
#        for m in obj['nodes'][canonical_input][sg_key]:                
#            
#            if sg_key == 'nodes_referenced':
#                sg_hash = str(abs(hash(t[1]+'->'+m)))
#                if tuplet_class.add_tuple(['sg_hash',sg_hash]) == []:
#                    ret_list.append( [1,t[0],t[1],m] )
#            elif sg_key == 'nodes_referenced_by':
#                sg_hash = str(abs(hash(m+'->'+t[2])))
#                if tuplet_class.add_tuple(['sg_hash',sg_hash]) == []:
#                    ret_list.append( [1,t[0],m,t[2]] )
#        #except:
#        #    pass
#            
#        return ret_list
    
    
def solve_alpha(t, limit=10):

    if len(t) < 2 or (len(t) == 2 and t[1].isupper()) or len(t) > 3:
        return []

    # alpha querysomething X
    if t[1].islower() and t[2][0].isupper():
        input_data = t[1]            
        raw_url = 'http://www.wolframalpha.com/input/?i=%s'
        enc_input = urllib.urlencode({'bla':input_data}).split('=')[1]
        url = raw_url % enc_input      
        try:      
            cont = urllib2.urlopen(url).read()
        except:
            time.sleep(2.0)
            cont = urllib2.urlopen(url).read()
        soup = BeautifulSoup(cont)
        try:
            res =  soup.find('img', id="i_0200_1")['alt']
        except:
            return []
        return [ [1,t[0],t[1],res] ]
    else:
        return []
  

def solve_auto_ar(t, limit=10):

    auto_attrs = [
                  'seccional',
                  'direccion',
                  'localidad',
                  'provincia',
                  'codigo_postal',
                  'telefono',
                  ]

    # auto_ar attributo patente
    # auto_ar attributo patente X
    if len(t) < 3 or len(t) > 4 :
        return []
    if not t[1] in auto_attrs:
        return []
    
    input_data = t[2].lower().replace('-','')
    input_data2 = t[1]
    
    url = 'https://sistemas.dnrpa.gov.ar/consultaintegral/ConsInve.php?consulta_externa=S'
    
    # tipo=A&dominio=ABC123&consulta_externa=S&SUBMIT=Consultar
    values = {'tipo' : 'A',
              'dominio' : input_data,
              'consulta_externa' : 'S',
              'SUBMIT' : 'Consultar'
             }
    
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    
    try:      
        cont = urllib2.urlopen(req).read()
    except:
        time.sleep(2.0)
        cont = urllib2.urlopen(req).read()
    
    print cont
        
    soup = BeautifulSoup(cont)
    try:
        res =  soup.findAll('font', face="Arial")
    except:
        return []
    
    if input_data2 == 'seccional':
        output = res[2].text
    elif input_data2 == 'direccion':
        output = res[4].text
    elif input_data2 == 'localidad':
        output = res[6].text
    elif input_data2 == 'provincia':
        output = res[8].text
    elif input_data2 == 'codigo_postal':
        output = res[10].text
    elif input_data2 == 'telefono':
        output = res[12].text
    else:
        return []

    output = sanitize(output)

    if len(t) == 3 or (len(t) == 4 and t[3][0].isupper()):
        return [ [1,t[0],t[1],t[2].lower(),output.lower()] ]
    elif t[3] == output.lower():
        return [ [1,t[0],t[1],t[2].lower(),output.lower()] ]
    else:
        return []
        
  
def solve_telefono_ar(t, limit=10):

    telefono_attrs = [
                  'nombre',
                  'domicilio',
                  ]

    # telefono_ar attributo telefono
    # telefono_ar attributo telefono X
    if len(t) < 3 or len(t) > 4 :
        return []
    if not t[1] in telefono_attrs:
        return []

    input_data = t[2].lower()
    telexplorer_attr = t[1]
    
    if ')' in input_data: # (011)444-45555 or (011)44445555
        area = input_data.split(')')[0].replace('(','').replace('-','')
        num = input_data.split(')')[1].replace('(','').replace('-','')
    elif '-' in input_data: # 011-4444-5555 or 011-44445555
        area = input_data.split('-')[0].replace('-','')
        num = ''.join(input_data.split('-')[1:])
    else: # 44445555
        area = '11'
        num = input_data
    
    while len(area)>0 and area[0] == '0':
        area = area[1:]
    
    
    url = 'http://www.telexplorer.com.ar/new/?zone=phoasp'
    
    # Submit=BUSCAR&area=11&telefono=42909105
    values = {'area' : area,
              'telefono' : num,
              'Submit' : 'BUSCAR',
             }
    
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    
    try:      
        cont = urllib2.urlopen(req).read()
    except:
        time.sleep(2.0)
        cont = urllib2.urlopen(req).read()
        
    soup = BeautifulSoup(cont)
    try:
        if telexplorer_attr == 'nombre':
            res =  soup.findAll(attrs={"class" : "resultado_titulo"})[0].text.lower()
        elif telexplorer_attr == 'domicilio':
            res =  soup.findAll(attrs={"class" : "resultado_domicilio"})[0].text.lower()
    except:
        return []

    if len(t) == 3 or (len(t) == 4 and t[3][0].isupper()):
        return [ [1,t[0],t[1],sanitize(t[2].lower()),res] ]
    elif t[3] == output.lower():
        return [ [1,t[0],t[1],sanitize(t[2].lower()),res] ]
    else:
        return []
  

def solve_persona_ar(t, limit=10):

    persona_attrs = [
                  'nombre',
                  'telefono',
                  'domicilio',
                  ]

    # telefono_ar attributo telefono
    # telefono_ar attributo telefono X
    if len(t) < 3 or len(t) > 4 :
        return []
    if not t[1] in persona_attrs:
        return []

    input_data = t[2].lower()
    telexplorer_attr = t[1]
    
    #url = 'http://www.telexplorer.com.ar/new/?zone=namwp'
    
    # Submit=BUSCAR&nombre=perez+juan&provincia=
#    values = {'nombre' : input_data,
#              'provincia' : '',
#              'Submit' : 'BUSCAR',
#             }
    
    #data = urllib.urlencode(values)
    #req = urllib2.Request(url, data)
    


    
    try:      
        br = mechanize.Browser()
        br.open('http://www.telexplorer.com.ar')
        br.select_form(nr=1)
        
        #br['Submit'] = 'BUSCAR'
        br['nombre'] = input_data
        br['provincia'] = []
        resp = br.submit()
        cont = resp.read()
    except:
        time.sleep(2.0)
        br = mechanize.Browser()
        br.open('http://www.telexplorer.com.ar')
        br.select_form(nr=1)
        
        #br['Submit'] = 'BUSCAR'
        br['nombre'] = input_data
        br['provincia'] = []
        resp = br.submit()
        cont = resp.read()
        
    soup = BeautifulSoup(cont)
    try:
        if telexplorer_attr == 'nombre':
            res =  soup.findAll(attrs={"class" : "resultado_titulo"})
        elif telexplorer_attr == 'domicilio':
            res =  soup.findAll(attrs={"class" : "resultado_domicilio"})
        elif telexplorer_attr == 'telefono':
            res =  soup.findAll(attrs={"class" : "resultado_telefono"})
    except:
        return []

    if len(t) == 3 or (len(t) == 4 and t[3][0].isupper()):
        return [ [1,t[0],t[1],t[2].lower(),sanitize(item.text.lower())] for item in res ]
    else:
        return []
  

def solve_twitter(t, limit=10):

    if len(t) < 2 or (len(t) == 2 and t[1].isupper()) or len(t) > 3:
        return []

    # twitter @user X
    new_t = []
    for e in t:
        if e[0] == '@':
            new_t.append(e.lower())
        else:
            new_t.append(e)
    t = new_t
    
    ret_list = []
    if t[1].islower() and t[2][0].isupper():
        ret_list = []
        twitter = twython.setup()
        #twitter = twython.setup(username="name", password="password")
        tl = []
        for i in range(3):
            try:
                tl = twitter.getUserTimeline(screen_name=t[1].replace('@',''), count=200)
                break
            except:
                time.sleep(float(2**i))
                continue
        for twit in tl:                
            txt = twit['text']
            #mentionhash = md5.new(t[1]+':'+txt).hexdigest().lower()
            mentionhash = str(abs(hash(t[1]+':'+txt)))
            try:
                if tuplet_class.add_tuple(['mentionhash1',mentionhash]) == []:
                    mentions = re.findall('@[a-zA-Z0-9_-]+',txt)
                    for mention in mentions:                    
                        ret_list.append( [1,t[0],t[1],mention.lower()] )
            except:
                pass
    # twitter X @user 
    elif t[1][0].isupper() and t[2].islower():
        ret_list = []
        twitter = twython.setup()
        tl = []
        for i in range(3):
            try:
                tl = twitter.searchTwitter(t[2].replace('@',''), rpp=100)
                break
            except:
                time.sleep(float(2**i))
                continue
        for twit in tl['results']:
            mention = twit['from_user'].lower()
            #mentionhash = md5.new('@'+mention+':'+twit['text']).hexdigest().lower()
            try:
                mentionhash = str(abs(hash('@'+mention+':'+twit['text'])))
                if tuplet_class.add_tuple(['mentionhash2',mentionhash]) == []:
                    ret_list.append( [1,t[0],'@'+mention,t[2]] )
            except:
                pass
    return ret_list


def solve_facebook(t, limit=10):
    
    attrs = [
             'name', 
             'sex', 
             'status', 
             'pic', 
             'birthday', 
             'first_name', 
             'last_name', 
             'pic_big', 
             'pic_small',
             'pic_square ',
             'pic',
             'affiliations',
             'profile_update_time',
             'religion',
             'birthday',
             'birthday_date',
             'meeting_sex',
             'username',
             'website',
             'profile_blurb',
             'verified',
             'allowed_restrictions',
             'profile_url',
             'locale',
             'online_presence',
             'is_app_user',
             'about_me',
             'quotes',
             'books',
             'movies',
             'tv',
             'music',
             'is_blocked',
             ]
    
    # facebook attr userid X
    if t[1].islower() and t[1] in attrs  and re.search('[0-9]+', t[2]).group() == t[2] and t[3][0].isupper():

        import facebook

        try:
            fb = facebook.Facebook(Secrets.get('facebook_key_1'), Secrets.get('facebook_key_2'))
            fb.session_key = Secrets.get('facebook_key_3')
            attrs = [t[1]]
            info = fb.users.getInfo([int(t[2])], attrs)
        except:
            return []
            #raise Exception('TupletsError: missing or wrongs keys for Facebook, or attribute &quot;%s&quot; invalid!' % t[1])
            #return [ [1,t[0],t[1],t[2], 'FACEBOOK_KEY_ERROR' ] ]
                
        
        if len(info) > 0 and t[1] in info[0] and info[0][t[1]] != None:
            
            if t[1] == 'status':
                
                if len(info[0][t[1]]['message']) == 0:
                    return []
                
                info[0][t[1]] = info[0][t[1]]['message']
                
            if t[1] == 'affiliations':                
                return [ [1,t[0],t[1],t[2], aff['name'] ] for aff in info[0][t[1]] ]

            if t[1] == 'profile_update_time':                
                return [ [1,t[0],t[1],t[2], time.ctime(int(info[0][t[1]])) ] ]
            
            if t[1] == 'religion' and len(info[0][t[1]]) == 0:                
                return []

            if bool(info[0][t[1]]) != info[0][t[1]] and list( info[0][t[1]] ) == info[0][t[1]] and len(info[0][t[1]]) > 0:
                return [ [1,t[0],t[1],t[2], metting_sex ] for metting_sex in info[0][t[1]] ]
            
            if str(info[0][t[1]] ) == info[0][t[1]] and len(info[0][t[1]]) == 0:
                return []
            
            return [ [1,t[0],t[1],t[2], str(info[0][t[1]]) ] ]
         
        # otherwise    
        return []
        

if __name__ == '__main__':

# persona_ar telefono [surname_and_name_from_argentina] X
#  print solve_persona_ar( ['persona_ar','telefono','doe john'] )
#  print solve_persona_ar( ['persona_ar','telefono','perversi angel'] )
#  print solve_persona_ar( ['persona_ar','telefono','orlicki jose'] )
#  print solve_persona_ar( ['persona_ar','telefono','orlicki viviana'] )
#  print solve_persona_ar( ['persona_ar','telefono','rampoldi maria'] )
  
  # auto_ar attributo patente X
  print solve_auto_ar( ['auto_ar','localidad','AUZ553'] )
