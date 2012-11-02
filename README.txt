(2010/10/18)

See the sample script (testPy.py) in order to see how
these methods are used. Remember that script needs to be set
to executable (+x) and that it has to be in the right 
location - e.g. cgi-bin

MaltegoEntity class:
---------------------
Used to construct an entity to be returned.

Methods:
	__init__(self,eT=None,v=None):
	setType(self,eT=None):
	setValue(self,eV=None):
	setWeight(self,w=None):
	setDisplayInformation(self,di=None):
	addAdditionalFields(self,fieldName=None,displayName=None,matchingRule=False,value=None):
	setIconURL(self,iU=None):
	returnEntity(self):



MaltegoTransform class:
---------------------
Used to send constructed entities back to the client.

Methods:
	addEntity(self,enType,enValue):
	addEntityToMessage(self,maltegoEntity):
	addUIMessage(self,message,messageType="Inform"):
	addException(self,exceptionString):
	throwExceptions(self):
	returnOutput(self):
	debug(self,msg):
			

MaltegoMsg class:
---------------------
Used to read incoming POST XML and break up into usable variables
Methods:
 	__init__(self,MaltegoXML=""):





