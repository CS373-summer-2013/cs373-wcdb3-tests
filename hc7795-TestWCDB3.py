#!/usr/bin/env python

"""
testWCDB.py

To test the program:
	% python testWCDB.py >& testWCDB.py.out
	% chmod ugo+x testWCDB.py
	% testWCDB.py >& testWCDB.py.out
"""


"""
Import.
"""

# ElementTree XML parsing.
try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

# minixsv XML validation and parsing.
from minixsv import pyxsval
from genxmlif import GenXmlIfError

# Setup Django environment.
from django.core.management import setup_environ
import settings
setup_environ(settings)

# Django code.
from django.db import models
from wcdb.models import Person, Organization, Crisis

# xmlParser code.
from xmlParser import getTextAndAttributes, getCommonData, elementTreeToModels, isNotDuplicate, indent

# Misc.
import logging
import StringIO
import unittest




# --------
# TestWCDB
# --------

class TestWCDB (unittest.TestCase):
	
	# def testXmlToModel_01(self):
	# 	raise Exception("No tests are implemented yet!")



	def testGetTextAndAttributes_01(self):
		testXML = """
			<element attribute1="a" attribute2="b" attribute3="c" attribute4="d">12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890</element>
		"""

		tree = ET.fromstring(testXML)
		it = tree.iter()
		pairs = getTextAndAttributes( it.next() )

		self.assert_(len(pairs) == 5)
		
		self.assert_( pairs["attribute1"] == "a" )
		self.assert_( pairs["attribute2"] == "b" )
		self.assert_( pairs["attribute3"] == "c" )
		self.assert_( pairs["attribute4"] == "d" )

		self.assert_( pairs["content"] == "12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890" )

		try:
			it.next()
			raise Exception("StopIteration exception should have been raised!")
		except StopIteration as e:
			pass



	def testGetTextAndAttributes_02(self):
		testXML = """
			<Person ID="PER_OSAMAB" Name="Osama Bin Laden">
			<Crises>
				<Crisis ID="CRI_NINEOO" />
			</Crises>
			<Organizations>
				<Org ID="ORG_AQAEDA" />
			</Organizations>
			<Kind>Founder of al-Qaeda</Kind>
			<Common>
				<ExternalLinks>
					 <li href="https://en.wikipedia.org/wiki/Osama_Bin_Laden">Wikipedia</li>
				</ExternalLinks>
				<Images>
					<li  embed="https://upload.wikimedia.org/wikipedia/commons/c/ca/Osama_bin_Laden_portrait.jpg" />
				</Images>
			</Common>
		</Person>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		it = tree.iter()
		e = it.next()
		pairs = getTextAndAttributes(e)

		self.assert_(len(pairs) == 2)

		self.assert_( pairs["ID"] == "PER_OSAMAB" )
		self.assert_( pairs["Name"] == "Osama Bin Laden" )

		# Advance iterator
		for i in range(10):
			e = it.next()

		try:
			it.next()
			raise Exception("StopIteration exception should have been raised!")
		except StopIteration as e:
			pass

	def testGetTextAndAttributes_03(self):
		testXML = """
			<Crisis ID="CRI_BAGAIR" Name="Baghdad Airstrike">
			<People>
				<Person ID="PER_BRAMAN" />
				<Person ID="PER_JULASS" />
			</People>
			<Organizations>
				<Org ID="ORG_WIKLKS" />
			</Organizations>
			<Kind>War</Kind>
			<Date>2007-07-12</Date>
			<Locations>
				<li>New Baghdad, Baghdad, Iraq</li>
			</Locations>
			<HumanImpact>
				<li>12 civilians died, 2 children wounded</li>
			</HumanImpact>
			<Common>
				<ExternalLinks>
					 <li href="https://en.wikipedia.org/wiki/July_12,_2007_Baghdad_airstrike">Wikipedia</li>
				</ExternalLinks>
			</Common>
		</Crisis>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		it = tree.iter()
		e = it.next()
		pairs = getTextAndAttributes(e)

		self.assert_(len(pairs) == 2)
		self.assert_( pairs["ID"] == "CRI_BAGAIR" )
		self.assert_( pairs["Name"] == "Baghdad Airstrike" )

		# Advance iterator
		for i in range(14):
			e = it.next()

		try:
			it.next()
			raise Exception("StopIteration exception should have been raised!")
		except StopIteration as e:
			pass

	def testgetCommonData_01(self):
		testXML = """
			<Common>
				<ExternalLinks>
					 <li href="https://en.wikipedia.org/wiki/Iraq_war">Wikipedia</li>
				</ExternalLinks>
				<Images>
					<li  embed="https://upload.wikimedia.org/wikipedia/commons/2/2e/Iraq_War_montage.png" />
				</Images>
			</Common>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		it = tree.iter()
		e = it.next()
		nextElement, treeIter, d = getCommonData(e, it)
		self.assert_(len(d) == 7)
		self.assert_(len(d["ExternalLinks"]) == 1)
		self.assert_( d["ExternalLinks"][0]["href"] == "https://en.wikipedia.org/wiki/Iraq_war" )
		self.assert_( d["Images"][0]["embed"] == "https://upload.wikimedia.org/wikipedia/commons/2/2e/Iraq_War_montage.png" )


		try:
			it.next()
			raise Exception("StopIteration exception should have been raised!")
		except StopIteration as e:
			pass

	def testgetCommonData_02(self):
		testXML = """
			<Common>
				<Citations>
					 <li href="http://iava.org/">Official Website</li>
					 <li  embed="http://patrickstjohn.org/images/iava-logo.jpg" />
				</Citations>
				<Images>
					<li  embed="http://patrickstjohn.org/images/iava-logo.jpg" />
				</Images>
				<Summary>
					It's an organization.
				</Summary>
			</Common>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		it = tree.iter()
		e = it.next()
		nextElement, treeIter, d = getCommonData(e, it)
		self.assert_(len(d) == 7)
		self.assert_(len(d["Citations"]) == 2)
		self.assert_( d["Citations"][0]["href"] == "http://iava.org/" )
		self.assert_( d["Citations"][1]["embed"] == "http://patrickstjohn.org/images/iava-logo.jpg" )
		self.assert_( d["Citations"][0]["content"] == "Official Website" )
		self.assert_( d["Images"][0]["embed"] == "http://patrickstjohn.org/images/iava-logo.jpg" )
		self.assert_( d["Summary"] == " It's an organization. " )


		try:
			it.next()
			raise Exception("StopIteration exception should have been raised!")
		except StopIteration as e:
			pass

	def testgetCommonData_03(self):
		testXML = """
			<Common>
				<ExternalLinks>
					<li href="http://www.fema.gov/">Official Website</li>
					<li embed="http://www.cdc.gov/">Official Website</li>
				</ExternalLinks>
				<Images>
					<li  embed="https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/FEMA_logo.svg/640px-FEMA_logo.svg.png" />
				</Images>
				<Videos>
					<li  embed="https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/FEMA_logo.svg/640px-FEMA_logo.svg.png" />
				</Videos>
				<Maps>
					<li  embed="https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/FEMA_logo.svg/640px-FEMA_logo.svg.png" />
				</Maps>
				<Feeds>
					<li  embed="https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/FEMA_logo.svg/640px-FEMA_logo.svg.png" />
				</Feeds>
				<Summary>
					hello
				</Summary>
			</Common>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		it = tree.iter()
		e = it.next()
		nextElement, treeIter, d = getCommonData(e, it)
		self.assert_(len(d) == 7)
		self.assert_(len(d["ExternalLinks"]) == 2)
		self.assert_( d["ExternalLinks"][0]["href"] == "http://www.fema.gov/" )
		self.assert_( d["ExternalLinks"][1]["embed"] == "http://www.cdc.gov/" )
		self.assert_( d["Images"][0]["embed"] == "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/FEMA_logo.svg/640px-FEMA_logo.svg.png" )
		self.assert_( d["Maps"][0]["embed"] == "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/FEMA_logo.svg/640px-FEMA_logo.svg.png" )
		self.assert_( d["Summary"] == " hello " )


		try:
			it.next()
			raise Exception("StopIteration exception should have been raised!")
		except StopIteration as e:
			pass



	def testelementTreeToModels_01(self):
		testXML = """
			<WorldCrises>
				<Crisis ID="CRI_HURIKE" Name="Hurricane Ike">
					<People>
						<Person ID="PER_RENPRE" />
					</People>
					<Organizations>
						<Org ID="ORG_FEDEMA" />
					</Organizations>
					<Kind>Natural Disaster</Kind>
					<Date>2008-09-01</Date>
					<Locations>
						<li>Turks and Caicos, Bahamas, Haiti, Dominican Republic, Cuba, Florida Keys, Mississippi, Louisiana, Texas, Mississippi Valley, Ohio Valley, Great Lakes region, Eastern Canada</li>
					</Locations>
					<HumanImpact>
						<li>Fatalities: 103 direct, 92 indirect</li>
					</HumanImpact>
					<EconomicImpact>
						<li>37.5 billion (2008 USD)</li>
					</EconomicImpact>
					<Common>
						<ExternalLinks>
							 <li href="https://en.wikipedia.org/wiki/Hurricane_Ike">Wikipedia</li>
						</ExternalLinks>
						<Images>
							<li  embed="https://upload.wikimedia.org/wikipedia/commons/c/c1/Hurricane_Ike_off_the_Lesser_Antilles.jpg" />
						</Images>
					</Common>
				</Crisis>
			</WorldCrises>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		dictionary={};
		models = elementTreeToModels(tree,dictionary)
		self.assert_(len(models) == 3)
		self.assert_( models[0][0].CrisisID == "CRI_HURIKE" )
		self.assert_( models[0][0].CrisisName == "Hurricane Ike" )
		self.assert_( models[0][0].crisisKind == "Natural Disaster" )
		self.assert_( models[0][0].crisisDate == "2008-09-01" )

	def testelementTreeToModels_02(self):
		testXML = """
			<WorldCrises>
				<Person ID="PER_GHARTL" Name="Gregory Hartl">
					<Crises>
						<Crisis ID="CRI_SWNFLU" />
					</Crises>
					<Organizations>
						<Org ID="ORG_WHLORG" />
					</Organizations>
					<Kind>Head of Public Relations/Social Media for World Health Organization</Kind>
					<Common>
						<ExternalLinks>
							 <li href="https://twitter.com/HaertlG">Twitter</li>
						</ExternalLinks>
						<Images>
							<li  embed="http://news.bbcimg.co.uk/media/images/67578000/jpg/_67578538_67578537.jpg" />
						</Images>
					</Common>
				</Person>
			</WorldCrises>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		dictionary={};
		models = elementTreeToModels(tree,dictionary)
		self.assert_(len(models[0]) == 0)
		self.assert_( models[1][0].PersonID == "PER_GHARTL" )
		self.assert_( models[1][0].PersonName == "Gregory Hartl" )
		self.assert_( models[1][0].personKind == "Head of Public Relations/Social Media for World Health Organization" )

	def testelementTreeToModels_03(self):
		testXML = """
			<WorldCrises>
				<Organization ID="ORG_UNICEF" Name="UNICEF">
					<Crises>
						<Crisis ID="CRI_WSAFRC" />
						<Crisis ID="CRI_HAITIE" />
					</Crises>
					<Kind>Humanitarian</Kind>
					<Location>New York, USA</Location>
					<History>
						<li>Founded in 1946</li>
					</History>
					<ContactInfo>
						<li>Phone: 1-800-FOR-KIDS</li>
					</ContactInfo>
					<Common>
						<ExternalLinks>
							 <li href="http://www.unicefusa.org/">Official Website</li>
						</ExternalLinks>
						<Images>
							<li  embed="https://upload.wikimedia.org/wikipedia/commons/d/d1/Flag_of_UNICEF.svg" />
						</Images>
					</Common>
				</Organization>
			</WorldCrises>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		dictionary={};
		models = elementTreeToModels(tree,dictionary)
		self.assert_(len(models[1]) == 0)
		self.assert_( models[2][0].OrganizationID == "ORG_UNICEF" )
		self.assert_( models[2][0].OrganizationName == "UNICEF" )
		self.assert_( models[2][0].orgKind == "Humanitarian" )

	def testisNotDuplicate_01(self):
		dictionary={1:"a",2:"b",3:"c"};
		b = isNotDuplicate("d","a",dictionary)
		self.assert_(b == True)

	def testisNotDuplicate_02(self):
		dictionary={1:"a",2:"b",3:"c"};
		b = isNotDuplicate("a","a",dictionary)
		self.assert_(b == False)

	def testisNotDuplicate_03(self):
		dictionary={1:"a",2:"b",3:"c"};
		b = isNotDuplicate("c","a",dictionary)
		self.assert_(b == False)


	def test_indent_01 (self) :
		testXML = """
			<WorldCrises>
			<Crisis ID="CRI_HURIKE" Name="Hurricane Ike">
			<Kind>Natural Disaster</Kind>
			<Date>2008-09-01</Date>
			</Crisis>
			</WorldCrises>
			"""
		testXML = " ".join(testXML.split())
		tree = ET.fromstring(testXML)
		indent(tree)
		indentReturned = ET.tostring(tree)
		#ans = '<WorldCrises>\n  <Crisis ID="CRI_HURIKE" Name="Hurricane Ike"\n    <Kind>Natural Disaster</Kind>\n    <Date>2008-09-01</Date>\n  </Crisis>\n</WorldCrises>'
		self.assert_(indentReturned != testXML)		

	def test_indent_02 (self) :
		testXML = """
			<Organization ID="ORG_CARERA" Name="Care">
			<Crises>
			<Crisis ID="CRI_WSAFRC" />
			</Crises>
			</Organization>
			"""
		testXML = " ".join(testXML.split())
		tree = ET.fromstring(testXML)
		indent(tree)
		indentReturned = ET.tostring(tree)
		#ans = '<Organization ID="ORG_CARERA" Name="Care">\n  <Crises>\n    <Crisis ID="CRI_WSAFRC" />\n  </Crises>\n</Organization>'
		self.assert_(indentReturned != testXML)
		
	def test_indent_03 (self) :
		testXML = """
			<Person ID="PER_BUSDAD" Name="George H. W. Bush">
			<Crises>
			<Crisis ID="CRI_EXXONV" />
			</Crises>
			<Kind>President of the United States</Kind>
			<Common>
			<ExternalLinks>
			<li href="https://en.wikipedia.org/wiki/George_H._W._Bush">Wikipedia</li>
			</ExternalLinks>
			<Images>
			<li embed="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/George_H._W._Bush%2C_President_of_the_United_States%2C_1989_official_portrait.jpg/520px-George_H._W._Bush%2C_President_of_the_United_States%2C_1989_official_portrait.jpg" />
			</Images>
			</Common>
			</Person>
			"""
		testXML = " ".join(testXML.split())
		tree = ET.fromstring(testXML)
		indent(tree)
		indentReturned = ET.tostring(tree)
		self.assert_(indentReturned != testXML)
		
	def testelementTreeToModels_01(self):
		testXML = """
		<WorldCrises>
			<Crisis ID="CRI_HURIKE" Name="Hurricane Ike">
				<People>
					<Person ID="PER_RENPRE" />
				</People>
				<Organizations>
					<Org ID="ORG_FEDEMA" />
				</Organizations>
				<Kind>Natural Disaster</Kind>
				<Date>2008-09-01</Date>
				<Locations>
					<li>Turks and Caicos, Bahamas, Haiti, Dominican Republic, Cuba, Florida Keys, Mississippi, Louisiana, Texas, Mississippi Valley, Ohio Valley, Great Lakes region, Eastern Canada</li>
				</Locations>
				<HumanImpact>
					<li>Fatalities: 103 direct, 92 indirect</li>
				</HumanImpact>
				<EconomicImpact>
					<li>37.5 billion (2008 USD)</li>
				</EconomicImpact>
				<Common>
					<ExternalLinks>
						  <li href="https://en.wikipedia.org/wiki/Hurricane_Ike">Wikipedia</li>
					</ExternalLinks>
					<Images>
						<li  embed="https://upload.wikimedia.org/wikipedia/commons/c/c1/Hurricane_Ike_off_the_Lesser_Antilles.jpg" />
					</Images>
				</Common>
			</Crisis>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)

		self.assert_( models[0][0].id == "CRI_HURIKE" )
		self.assert_( models[0][0].name == "Hurricane Ike" )
		self.assert_( models[0][0].kind == "Natural Disaster" )
		self.assert_( models[0][0].date == "2008-09-01" )
		self.assert_( models[0][0].location == "['Turks and Caicos, Bahamas, Haiti, Dominican Republic, Cuba, Florida Keys, Mississippi, Louisiana, Texas, Mississippi Valley, Ohio Valley, Great Lakes region, Eastern Canada']" )
		self.assert_( models[0][0].humanImpact == "['Fatalities: 103 direct, 92 indirect']" )
		self.assert_( models[0][0].economicImpact == "['37.5 billion (2008 USD)']" )
		self.assert_( models[0][0].people == "['PER_RENPRE']" )
		self.assert_( models[0][0].organizations == "['ORG_FEDEMA']" )
		self.assert_( models[0][0].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Hurricane_Ike")
		self.assert_( models[0][0].common.externalLinks.all()[0].content == "Wikipedia")
		self.assert_( models[0][0].common.images.all()[0].embed == "https://upload.wikimedia.org/wikipedia/commons/c/c1/Hurricane_Ike_off_the_Lesser_Antilles.jpg")
		
		
	def testelementTreeToModels_02(self):
		testXML = """
		<WorldCrises>
			<Person ID="PER_BRAMAN" Name="Bradley Manning">
				<Crises>
					<Crisis ID="CRI_BAGAIR" />
				</Crises>
				<Organizations>
					<Org ID="ORG_IAVETA" />
				</Organizations>
				<Kind>Private First Class</Kind>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/Bradley_Manning">Wikipedia</li>
					</ExternalLinks>
					<Images>
						<li  embed="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Bradley_Manning_US_Army.jpg/614px-Bradley_Manning_US_Army.jpg" />
					 </Images>
				</Common>
			</Person>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)
		
		self.assert_( models[1][0].id == "PER_BRAMAN" )
		self.assert_( models[1][0].name == "Bradley Manning" )
		self.assert_( models[1][0].crises == "['CRI_BAGAIR']" )
		self.assert_( models[1][0].organizations == "['ORG_IAVETA']" )
		self.assert_( models[1][0].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Bradley_Manning")
		self.assert_( models[1][0].common.externalLinks.all()[0].content == "Wikipedia")
		self.assert_( models[1][0].common.images.all()[0].embed == "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Bradley_Manning_US_Army.jpg/614px-Bradley_Manning_US_Army.jpg")
		
	def testelementTreeToModels_03(self):
		testXML = """
		<WorldCrises>
			<Organization ID="ORG_AQAEDA" Name="al-Qaeda">
				<Crises>
					<Crisis ID="CRI_IRAQWR" />
					<Crisis ID="CRI_NINEOO" />
				 </Crises>
				 <People>
					<Person ID="PER_OSAMAB" />
				  </People>
				  <Kind>Terrorist</Kind>
				  <Location>World Wide</Location>
				  <History>
					  <li>Founded in 1988</li>
				  </History>
				  <Common>
					  <ExternalLinks>
						  <li href="https://en.wikipedia.org/wiki/Al_Queda">Wikipedia</li>
					  </ExternalLinks>
				  </Common>
			</Organization>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)
		self.assert_( models[2][0].id == "ORG_AQAEDA" )
		self.assert_( models[2][0].name == "al-Qaeda" )
		self.assert_( models[2][0].kind == "Terrorist" )
		self.assert_( models[2][0].location == "World Wide" )
		self.assert_( str(models[2][0].history) == "['Founded in 1988']" )
		self.assert_( models[2][0].crises == "['CRI_IRAQWR', 'CRI_NINEOO']" )
		self.assert_( models[2][0].people == "['PER_OSAMAB']" )
		self.assert_( models[2][0].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Al_Queda")
		self.assert_( models[2][0].common.externalLinks.all()[0].content == "Wikipedia")
		
	def testelementTreeToModels_04(self):
		testXML = """
		<WorldCrises>
			<Crisis ID="CRI_SWNFLU" Name="Influenza A virus subtype H1N1">
				<People>
					<Person ID="PER_BROBMA" />
					<Person ID="PER_GHARTL" />
				</People>
				<Organizations>
					<Org ID="ORG_WHLORG" />
					<Org ID="ORG_CFDCAP" />
					<Org ID="ORG_REDCRS" />
				</Organizations>
				<Kind>Pandemic</Kind>
				<Date>2009-10-01</Date>
				<Locations>
					<li>World Wide</li>
				</Locations>
				<HumanImpact>
					<li>caused severe illness in 3 to 5 million people</li>
					<li>250,000 to 500,000 deaths worldwide</li>
				</HumanImpact>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/2009_flu_pandemic">Wikipedia</li>
					</ExternalLinks>
					<Images>
						<li  embed="https://upload.wikimedia.org/wikipedia/commons/f/f0/H1N1_influenza_virus.jpg" />
					</Images>
				</Common>
			</Crisis>
			<Crisis ID="CRI_EXXONV" Name="Exxon Valdez Oil Spill">
				<People>
					<Person ID="PER_BUSDAD" />
				</People>
				<Organizations>
					<Org ID="ORG_OILREC" />
				</Organizations>
				<Kind>Oil Spill</Kind>
				<Date>1989-03-24</Date>
				<Locations>
					<li>Prince William Sound, Alaska</li>
				</Locations>
				<HumanImpact>
					<li>devastated fishing industry</li>
				</HumanImpact>
				<EconomicImpact>
					<li>$3.8 billion in clean cup costs, fines, compensation</li>
				</EconomicImpact>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/Exxon_Valdez_oil_spill">Wikipedia</li>
					</ExternalLinks>
					<Images>
						<li  embed="https://upload.wikimedia.org/wikipedia/commons/6/66/Exval.jpeg" />
					</Images>
				</Common>
			</Crisis>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)

		self.assert_( models[0][0].id == "CRI_SWNFLU" )
		self.assert_( models[0][0].name == "Influenza A virus subtype H1N1" )
		self.assert_( models[0][0].kind == "Pandemic" )
		self.assert_( models[0][0].date == "2009-10-01" )
		self.assert_( models[0][0].location == "['World Wide']" )
		self.assert_( models[0][0].humanImpact == "['caused severe illness in 3 to 5 million people', '250,000 to 500,000 deaths worldwide']" )
		self.assert_( models[0][0].people == "['PER_BROBMA', 'PER_GHARTL']" )
		self.assert_( models[0][0].organizations == "['ORG_WHLORG', 'ORG_CFDCAP', 'ORG_REDCRS']" )
		self.assert_( models[0][0].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/2009_flu_pandemic")
		self.assert_( models[0][0].common.externalLinks.all()[0].content == "Wikipedia")
		self.assert_( models[0][0].common.images.all()[0].embed == "https://upload.wikimedia.org/wikipedia/commons/f/f0/H1N1_influenza_virus.jpg")
		
		self.assert_( models[0][1].id == "CRI_EXXONV" )
		self.assert_( models[0][1].name == "Exxon Valdez Oil Spill" )
		self.assert_( models[0][1].kind == "Oil Spill" )
		self.assert_( models[0][1].date == "1989-03-24" )
		self.assert_( models[0][1].location == "['Prince William Sound, Alaska']" )
		self.assert_( models[0][1].humanImpact == "['devastated fishing industry']" )
		self.assert_( models[0][1].economicImpact == "['$3.8 billion in clean cup costs, fines, compensation']" )
		self.assert_( models[0][1].people == "['PER_BUSDAD']" )
		self.assert_( models[0][1].organizations == "['ORG_OILREC']" )
		self.assert_( models[0][1].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Exxon_Valdez_oil_spill")
		self.assert_( models[0][1].common.externalLinks.all()[0].content == "Wikipedia")
		self.assert_( models[0][1].common.images.all()[0].embed == "https://upload.wikimedia.org/wikipedia/commons/6/66/Exval.jpeg")
		
		
		
	def testelementTreeToModels_05(self):
		testXML = """
		<WorldCrises>
			<Person ID="PER_SADHUS" Name="Saddam Hussein">
				<Crises>
					<Crisis ID="CRI_IRAQWR" />
				</Crises>
				<Kind>President of Iraq</Kind>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/Saddam_Hussein">Wikipedia</li>
					</ExternalLinks>
					<Images>
						<li  embed="https://upload.wikimedia.org/wikipedia/commons/f/f1/Iraq%2C_Saddam_Hussein_%28222%29.jpg" />
					</Images>
				</Common>
			</Person>

			<Person ID="PER_OSAMAB" Name="Osama Bin Laden">
				<Crises>
					<Crisis ID="CRI_NINEOO" />
				</Crises>
				<Organizations>
					<Org ID="ORG_AQAEDA" />
				</Organizations>
				<Kind>Founder of al-Qaeda</Kind>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/Osama_Bin_Laden">Wikipedia</li>
					</ExternalLinks>
					<Images>
						<li  embed="https://upload.wikimedia.org/wikipedia/commons/c/ca/Osama_bin_Laden_portrait.jpg" />
					</Images>
				</Common>
			</Person>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)

		self.assert_( models[1][0].id == "PER_SADHUS" )
		self.assert_( models[1][0].name == "Saddam Hussein" )
		self.assert_( models[1][0].kind == "President of Iraq" )
		self.assert_( models[1][0].crises == "['CRI_IRAQWR']")
		self.assert_( models[1][0].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Saddam_Hussein")
		self.assert_( models[1][0].common.externalLinks.all()[0].content == "Wikipedia")
		self.assert_( models[1][0].common.images.all()[0].embed == "https://upload.wikimedia.org/wikipedia/commons/f/f1/Iraq%2C_Saddam_Hussein_%28222%29.jpg")
		
		self.assert_( models[1][1].id == "PER_OSAMAB" )
		self.assert_( models[1][1].name == "Osama Bin Laden" )
		self.assert_( models[1][1].kind == "Founder of al-Qaeda" )
		self.assert_( models[1][1].crises == "['CRI_NINEOO']")
		self.assert_( models[1][1].organizations == "['ORG_AQAEDA']" )
		self.assert_( models[1][1].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Osama_Bin_Laden")
		self.assert_( models[1][1].common.externalLinks.all()[0].content == "Wikipedia")
		self.assert_( models[1][1].common.images.all()[0].embed == "https://upload.wikimedia.org/wikipedia/commons/c/ca/Osama_bin_Laden_portrait.jpg")
	
	def testelementTreeToModels_06(self):
		testXML = """
		<WorldCrises>
			<Organization ID="ORG_WIKLKS" Name="Wikileaks">
				<Crises>
					<Crisis ID="CRI_BAGAIR" />
				</Crises>
				<People>
					<Person ID="PER_JULASS" />
				</People>
				<Kind>Nonprofit document archive and disclosure</Kind>
				<Location>Online</Location>
				<History>
					<li>Launched in 2006</li>
				</History>
				<ContactInfo>
					<li>IRC: http://chat.wikileaks.org/</li>
				</ContactInfo>
				<Common>
					<ExternalLinks>
						<li href="http://wikileaks.org/">Official Website</li>
					</ExternalLinks>
					<Images>
						<li  embed="http://wikileaks.org/IMG/wlogo.png" />
					</Images>
				</Common>
			</Organization>
			<Organization ID="ORG_AQAEDA" Name="al-Qaeda">
				<Crises>
					<Crisis ID="CRI_IRAQWR" />
					<Crisis ID="CRI_NINEOO" />
				</Crises>
				<People>
					<Person ID="PER_OSAMAB" />
				</People>
				<Kind>Terrorist</Kind>
				<Location>World Wide</Location>
				<History>
					<li>Founded in 1988</li>
				</History>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/Al_Queda">Wikipedia</li>
					</ExternalLinks>
				</Common>
			</Organization>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)

		self.assert_( models[2][0].id == "ORG_WIKLKS" )
		self.assert_( models[2][0].name == "Wikileaks" )
		self.assert_( models[2][0].kind == "Nonprofit document archive and disclosure" )
		self.assert_( models[2][0].location == "Online")
		self.assert_( models[2][0].crises == "['CRI_BAGAIR']")
		self.assert_( models[2][0].people == "['PER_JULASS']")
		self.assert_( models[2][0].common.externalLinks.all()[0].href == "http://wikileaks.org/")
		self.assert_( models[2][0].common.externalLinks.all()[0].content == "Official Website")
		self.assert_( models[2][0].common.images.all()[0].embed == "http://wikileaks.org/IMG/wlogo.png")
		
		self.assert_( models[2][1].id == "ORG_AQAEDA" )
		self.assert_( models[2][1].name == "al-Qaeda" )
		self.assert_( models[2][1].kind == "Terrorist" )
		self.assert_( models[2][1].crises == "['CRI_IRAQWR', 'CRI_NINEOO']")
		self.assert_( str(models[2][1].history) == "['Founded in 1988']")
		self.assert_( models[2][1].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Al_Queda")
		self.assert_( models[2][1].common.externalLinks.all()[0].content == "Wikipedia")
	
	
	def testelementTreeToModels_07(self):
		testXML = """
		<WorldCrises>
			<Organization ID="ORG_WIKLKS" Name="wowo">
				<Crises>
					<Crisis ID="CRI_BAGAIR" />
				</Crises>
				<People>
					<Person ID="PER_JULASS" />
				</People>
				<Kind>Nonprofit document archive and disclosure</Kind>
				<Location>Online</Location>
				<History>
					<li>Launched in 2006</li>
				</History>
				<ContactInfo>
					<li>IRC: http://chat.wikileaks.org/</li>
				</ContactInfo>
				<Common>
					<ExternalLinks>
						<li href="http://wikileaks.org/">Official Website</li>
					</ExternalLinks>
					<Images>
						<li  embed="http://wikileaks.org/IMG/wlogo.png" />
					</Images>
				</Common>
			</Organization>
			<Organization ID="ORG_AQAEDA" Name="al-Qaeda">
				<Crises>
					<Crisis ID="CRI_IRAQWR" />
					<Crisis ID="CRI_NINEOO" />
				</Crises>
				<People>
					<Person ID="PER_OSAMAB" />
				</People>
				<Kind>Terrorist</Kind>
				<Location>World Wide</Location>
				<History>
					<li>Founded in 1988</li>
				</History>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/Al_Queda">Wikipedia</li>
					</ExternalLinks>
				</Common>
			</Organization>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)

		self.assert_( models[2][0].id == "ORG_WIKLKS" )
		self.assert_( models[2][0].name == "wowo" )
		self.assert_( models[2][0].kind == "Nonprofit document archive and disclosure" )
		self.assert_( models[2][0].location == "Online")
		self.assert_( models[2][0].crises == "['CRI_BAGAIR']")
		self.assert_( models[2][0].people == "['PER_JULASS']")
		self.assert_( models[2][0].common.externalLinks.all()[0].href == "http://wikileaks.org/")
		self.assert_( models[2][0].common.externalLinks.all()[0].content == "Official Website")
		self.assert_( models[2][0].common.images.all()[0].embed == "http://wikileaks.org/IMG/wlogo.png")
		
		self.assert_( models[2][1].id == "ORG_AQAEDA" )
		self.assert_( models[2][1].name == "al-Qaeda" )
		self.assert_( models[2][1].kind == "Terrorist" )
		self.assert_( models[2][1].crises == "['CRI_IRAQWR', 'CRI_NINEOO']")
		self.assert_( str(models[2][1].history) == "['Founded in 1988']")
		self.assert_( models[2][1].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Al_Queda")
		self.assert_( models[2][1].common.externalLinks.all()[0].content == "Wikipedia")
		
	def testelementTreeToModels_08(self):
		testXML = """
		<WorldCrises>
			<Person ID="PER_BRAMAN" Name="Bradley Manning">
				<Crises>
					<Crisis ID="CRI_BAGAIR" />
					<Crisis ID="CRI_JOJOJA" />
				</Crises>
				<Organizations>
					<Org ID="ORG_IAVETA" />
				</Organizations>
				<Kind>Private First Class</Kind>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/Bradley_Manning">Wikipedia</li>
					</ExternalLinks>
					<Images>
						<li  embed="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Bradley_Manning_US_Army.jpg/614px-Bradley_Manning_US_Army.jpg" />
					 </Images>
				</Common>
			</Person>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)
		
		self.assert_( models[1][0].id == "PER_BRAMAN" )
		self.assert_( models[1][0].name == "Bradley Manning" )
		self.assert_( models[1][0].crises == "['CRI_BAGAIR', 'CRI_JOJOJA']" )
		self.assert_( models[1][0].organizations == "['ORG_IAVETA']" )
		self.assert_( models[1][0].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Bradley_Manning")
		self.assert_( models[1][0].common.externalLinks.all()[0].content == "Wikipedia")
		self.assert_( models[1][0].common.images.all()[0].embed == "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Bradley_Manning_US_Army.jpg/614px-Bradley_Manning_US_Army.jpg")
		
		
	def testelementTreeToModels_09(self):
		testXML = """
		<WorldCrises>
			<Person ID="PER_BRAMAN" Name="Bradley Manning">
				<Crises>
					<Crisis ID="CRI_BAGAIR" />
					<Crisis ID="CRI_JOJOJA" />
					<Crisis ID="CRI_HATARA" />
				</Crises>
				<Organizations>
					<Org ID="ORG_IAVETA" />
				</Organizations>
				<Kind>Private First Class</Kind>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/Bradley_Manning">Wikipedia</li>
					</ExternalLinks>
					<Images>
						<li  embed="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Bradley_Manning_US_Army.jpg/614px-Bradley_Manning_US_Army.jpg" />
					 </Images>
				</Common>
			</Person>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)
		
		self.assert_( models[1][0].id == "PER_BRAMAN" )
		self.assert_( models[1][0].name == "Bradley Manning" )
		self.assert_( models[1][0].crises == "['CRI_BAGAIR', 'CRI_JOJOJA', 'CRI_HATARA']" )
		self.assert_( models[1][0].organizations == "['ORG_IAVETA']" )
		self.assert_( models[1][0].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Bradley_Manning")
		self.assert_( models[1][0].common.externalLinks.all()[0].content == "Wikipedia")
		self.assert_( models[1][0].common.images.all()[0].embed == "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Bradley_Manning_US_Army.jpg/614px-Bradley_Manning_US_Army.jpg")
		
		
	def testelementTreeToModels_22(self):
		testXML = """
		<WorldCrises>
			<Person ID="PER_BRAMAN" Name="Bradley Manning">
				<Crises>
					<Crisis ID="CRI_BAGAIR" />
					<Crisis ID="CRI_JOJOJA" />
					<Crisis ID="CRI_HATARA" />
				</Crises>
				<Organizations>
					<Org ID="ORG_IAVETA" />
				</Organizations>
				<Kind>Private First Class</Kind>
				<Common>
					<ExternalLinks>
						<li href="https://en.wikipedia.org/wiki/Bradley_Manning">Wikipedia</li>
					</ExternalLinks>
					<Images>
						<li  embed="https://upload.wikimedia.fjgjf.dsgfg.com" />
					 </Images>
				</Common>
			</Person>
		</WorldCrises>
		"""
		testXML = " ".join(testXML.split())
		
		tree = ET.fromstring(testXML)
		dictionary={}
		models = elementTreeToModels(tree,dictionary)
		
		self.assert_( models[1][0].id == "PER_BRAMAN" )
		self.assert_( models[1][0].name == "Bradley Manning" )
		self.assert_( models[1][0].crises == "['CRI_BAGAIR', 'CRI_JOJOJA', 'CRI_HATARA']" )
		self.assert_( models[1][0].organizations == "['ORG_IAVETA']" )
		self.assert_( models[1][0].common.externalLinks.all()[0].href == "https://en.wikipedia.org/wiki/Bradley_Manning")
		self.assert_( models[1][0].common.externalLinks.all()[0].content == "Wikipedia")
		self.assert_( models[1][0].common.images.all()[0].embed == "https://upload.wikimedia.fjgjf.dsgfg.com")


print "TestWCDB.py"
unittest.main()
print "Done."
