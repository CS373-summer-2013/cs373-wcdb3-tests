"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from datetime import date
from django.test import TestCase
import sys
import StringIO
from django.test.simple import DjangoTestSuiteRunner
from django.http import HttpResponse
from django.conf import settings
from wcdb_export import xml_mods2etree, xml_etree2xml
from wcdb_import import xml_validate, xml_reader, xml_etree2mods, xml_merge
from wcdb_query import query_obama, query_people_without_orgs, query_things_without_pictures, query_crises_without_things, query_find_natural_disasters, query_people_with_many_crises, query_orgs_with_many_videos, query_people_in_crises_after_millenium, query_people_with_red_cross_videos, query_number_images_before_millenium 
from views import search_one_word
from models import People, Crises, Organizations, List_Item
import xml.etree.ElementTree as ET
#import unittest
from types import *

class SimpleTest(TestCase):

	# ------------
	# xml_validate
	# ------------

	def test_xml_validate_1(self) :
		xml_file   = open('wcdb/WCDB2.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		self.assertEqual(xml_validate(xml_file, xml_schema), True)
			
	def test_xml_validate_2(self) :
		xml_file   = open('wcdb/WCDB2Fail.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		self.assertEqual(xml_validate(xml_file, xml_schema), False)
	
	def test_xml_validate_3(self) :
		try :
			xml_file   = open('wcdb/models.py', 'r')
			xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
			self.assertEqual(xml_validate(xml_file, xml_schema), False)
			assert(False)
		except Exception :
			assert(True)
			
	
	# ----------
	# xml_reader
	# ----------

	def test_xml_reader_1(self) :
		xml_file   = open('wcdb/WCDB2.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		et = xml_reader(xml_file, xml_schema)
		self.assertEqual(type(et), type(ET.ElementTree('')))

	def test_xml_reader_2(self) :
		xml_file   = open('wcdb/WCDB2Fail.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		et = xml_reader(xml_file, xml_schema)
		self.assertTrue(et, 1)	
	
	def test_xml_reader_3(self) :
		xml_file   = open('wcdb/WCDB2.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		et = xml_reader(xml_file, xml_schema)
		self.assertEqual(type(et), type(ET.ElementTree('')))
		
		crisis_cnt = 0
		person_cnt = 0
		org_cnt    = 0
		for child in list(et.getroot()) :
			if child.tag == "Crisis" :
				crisis_cnt += 1
			elif child.tag == "Organization" :
				org_cnt += 1
			elif child.tag == "Person" :
				person_cnt += 1

		self.assertEqual(crisis_cnt, 10)
		self.assertEqual(person_cnt, 11)
		self.assertEqual(org_cnt,    11)


	# --------------
	# xml_etree2mods
	# --------------
        


	def test_etree2mods_1(self) :
		xml_file   = open('wcdb/WCDB2.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		et = xml_reader(xml_file, xml_schema)
		self.assertEqual(type(et), type(ET.ElementTree('')))
		xml_etree2mods(et.getroot())
		
		self.assertTrue(len(People.objects.all()) > 0)
		self.assertTrue(len(Crises.objects.all()) > 0)
		self.assertTrue(len(Organizations.objects.all()) > 0)
		self.assertTrue(len(List_Item.objects.all()) > 0)
		
	def test_etree2mods_2(self) :
		our_ids = [ 'CRI_CHINAD', 'CRI_SCMARI', 'CRI_NKCONF', 'CRI_FINCRI', 'CRI_HUMTRA',
					'CRI_EGYPTR', 'CRI_AIDSHI', 'CRI_AZWILD', 'CRI_LRACON', 'CRI_OSLOSH',
					'PER_MMORSI', 'PER_LALOCA', 'PER_GASPAR', 'PER_CYLUNG', 'PER_JKERRY',
					'PER_BROBMA', 'PER_MAGICJ', 'PER_COPETE', 'PER_VPUTIN', 'PER_JEABEL', 'PER_JONGUN',
					'ORG_MAMFDN', 'ORG_FIREDP', 'ORG_PARIBS', 'ORG_ASEANA', 'ORG_POLARS',
					'ORG_IMFUND', 'ORG_UNINAT', 'ORG_RIBBON', 'ORG_SALARM', 'ORG_WHORGN', 'ORG_CHILDR']
		xml_file   = open('wcdb/WCDB2.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		et = xml_reader(xml_file, xml_schema)
		self.assertEqual(type(et), type(ET.ElementTree('')))
		xml_etree2mods(et.getroot())
		
		people = People.objects.all()

		for p in people :
			self.assertEqual(p.idref in our_ids, True)		
	
	def test_etree2mods_3(self) :
		our_ids = [ 'CRI_CHINAD', 'CRI_SCMARI', 'CRI_NKCONF', 'CRI_FINCRI', 'CRI_HUMTRA',
					'CRI_EGYPTR', 'CRI_AIDSHI', 'CRI_AZWILD', 'CRI_LRACON', 'CRI_OSLOSH',
					'PER_MMORSI', 'PER_LALOCA', 'PER_GASPAR', 'PER_CYLUNG', 'PER_JKERRY',
					'PER_BROBMA', 'PER_MAGICJ', 'PER_COPETE', 'PER_VPUTIN', 'PER_JEABEL', 'PER_JONGUN',
					'ORG_MAMFDN', 'ORG_FIREDP', 'ORG_PARIBS', 'ORG_ASEANA', 'ORG_POLARS',
					'ORG_IMFUND', 'ORG_UNINAT', 'ORG_RIBBON', 'ORG_SALARM', 'ORG_WHORGN', 'ORG_CHILDR']
		xml_file   = open('wcdb/WCDB2.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		et = xml_reader(xml_file, xml_schema)
		self.assertEqual(type(et), type(ET.ElementTree('')))
		xml_etree2mods(et.getroot())
		
		orgs = Organizations.objects.all()

		for o in orgs :
			self.assertEqual(o.idref in our_ids, True)		
	
	def test_etree2mods_4(self) :
		our_ids = [ 'CRI_CHINAD', 'CRI_SCMARI', 'CRI_NKCONF', 'CRI_FINCRI', 'CRI_HUMTRA',
					'CRI_EGYPTR', 'CRI_AIDSHI', 'CRI_AZWILD', 'CRI_LRACON', 'CRI_OSLOSH',
					'PER_MMORSI', 'PER_LALOCA', 'PER_GASPAR', 'PER_CYLUNG', 'PER_JKERRY',
					'PER_BROBMA', 'PER_MAGICJ', 'PER_COPETE', 'PER_VPUTIN', 'PER_JEABEL', 'PER_JONGUN',
					'ORG_MAMFDN', 'ORG_FIREDP', 'ORG_PARIBS', 'ORG_ASEANA', 'ORG_POLARS',
					'ORG_IMFUND', 'ORG_UNINAT', 'ORG_RIBBON', 'ORG_SALARM', 'ORG_WHORGN', 'ORG_CHILDR']
		xml_file   = open('wcdb/WCDB2.xml', 'r')
		xml_schema = open('wcdb/WCDB2.xsd.xml', 'r')
		et = xml_reader(xml_file, xml_schema)
		self.assertEqual(type(et), type(ET.ElementTree('')))
		xml_etree2mods(et.getroot())
		
		crises = Crises.objects.all()

		for c in crises :
			self.assertEqual(c.idref in our_ids, True)		
	
	# ------
	# models
	# ------
	
	def test_tables_exist(self) :
		self.assertTrue(len(People.objects.all()) == 0)
		self.assertTrue(len(Crises.objects.all()) == 0)
		self.assertTrue(len(Organizations.objects.all()) == 0)
		self.assertTrue(len(List_Item.objects.all()) == 0)
		People(idref="PER_BROBMA", name="Barack Obama").save()
		
		self.assertTrue(len(People.objects.all()) == 1)
		self.assertTrue(len(Crises.objects.all()) == 0)
		self.assertTrue(len(Organizations.objects.all()) == 0)
		self.assertTrue(len(List_Item.objects.all()) == 0)

		Crises(idref="CRI_CHINAD", name="Chinese Democracy").save()

		self.assertTrue(len(People.objects.all()) == 1)
		self.assertTrue(len(Crises.objects.all()) == 1)
		self.assertTrue(len(Organizations.objects.all()) == 0)
		self.assertTrue(len(List_Item.objects.all()) == 0)

		Organizations(idref="ORG_FIREDP", name="Fire Department").save()

		self.assertTrue(len(People.objects.all()) == 1)
		self.assertTrue(len(Crises.objects.all()) == 1)
		self.assertTrue(len(Organizations.objects.all()) == 1)
		self.assertTrue(len(List_Item.objects.all()) == 0)

		List_Item(idref="ORG_FIREDP", list_type="Videos").save()

		self.assertTrue(len(People.objects.all()) == 1)
		self.assertTrue(len(Crises.objects.all()) == 1)
		self.assertTrue(len(Organizations.objects.all()) == 1)
		self.assertTrue(len(List_Item.objects.all()) == 1)

	# -------------
	# xml_etree2xml
	# -------------

	def test_xml_etree2xml_1(self) :
		dude = People(idref="PER_JAMESK", name="James Kunze", kind="Person who cleans up all your broken tests")
		dude.save()
		et = xml_mods2etree()
		xml_text = xml_etree2xml(et).decode('ascii')
		self.assertTrue(type(xml_text) is UnicodeType)
		obama = People(idref="PER_BROBMA", name="Barack Obama", kind="President")
		obama.save()
		et = xml_mods2etree()
		xml_text = xml_etree2xml(et).decode('ascii')
		self.assertTrue(type(xml_text) is UnicodeType)
	
	def test_xml_etree2xml_2(self) :
		root = ET.Element("Tag1")
		sub = ET.Element("Tag2")
		root.append(sub)
		et = ET.ElementTree(root)

		output = "<Tag1>\n\t<Tag2></Tag2 >\n</Tag1 >"
		
		xml_text = xml_etree2xml(et)
		self.assertEqual(xml_text == output, True)
	
	# --------------
	# xml_mods2etree
	# --------------

	def test_xml_mods2etree_1(self):
		et = xml_mods2etree()
		root = et.getroot()
		self.assertEqual(type(et), type(ET.ElementTree('')))
		self.assertEqual(root.tag, 'WorldCrises')


		for child in list(root) :
			valid = child.tag == "Crisis" or child.tag == "Organization" or child.tag == "Person"
			self.assertEqual(valid, True)

	def test_xml_mods2etree_2(self):
		et = xml_mods2etree()
		root = et.getroot()
		self.assertEqual(type(et), type(ET.ElementTree('')))
		self.assertEqual(root.tag, 'WorldCrises')
		crisis_cnt = 0
		person_cnt = 0
		org_cnt    = 0
		for child in list(root) :
			if child.tag == "Crisis" :
				crisis_cnt += 1
			elif child.tag == "Organization" :
				org_cnt += 1
			elif child.tag == "Person" :
				person_cnt += 1

		self.assertEqual(crisis_cnt, 0)
		self.assertEqual(person_cnt, 0)
		self.assertEqual(org_cnt,    0)

	# fails because mods2etree has been changed to no longer care for our_ids
	# double check
	def test_xml_mods2etree_3(self):
		p = People(idref="PER_TCANNO", name="Taylor Cannon", kind="badass")
		p.save()
		et = xml_mods2etree()
		root = et.getroot()
		self.assertEqual(type(et), type(ET.ElementTree('')))
		self.assertEqual(root.tag, 'WorldCrises')
		crisis_cnt = 0
		person_cnt = 0
		org_cnt    = 0
		for child in list(root) :
			if child.tag == "Crisis" :
				crisis_cnt += 1
			elif child.tag == "Organization" :
				org_cnt += 1
			elif child.tag == "Person" :
				person_cnt += 1

		self.assertEqual(crisis_cnt, 0)
		self.assertEqual(person_cnt, 1)
		self.assertEqual(org_cnt,    0)

 	# --------------
	# query_obama
	# --------------

	def test_query_obama(self):
		query_obama()

		obama = People(idref="PER_BROBMA", name="Barack Obama")
		steve = People(idref="PER_STEVEN", name="Steve")
		robert = People(idref="PER_ROBERT", name="Robert")
		moon = People(idref="PER_MOOOON", name="The Moon")
		picnic = Crises(idref="CRI_PICNIC", name="A Picnic")
		aliens = Organizations(idref="ORG_ALIENS", name="Aliens")
		obama.save()
		steve.save()
		robert.save()
		moon.save()
		picnic.save()
		aliens.save()

		picnic.people.add(obama)
		picnic.people.add(steve)

		obama.organizations.add(aliens)
		robert.organizations.add(aliens)

		result = query_obama()

		self.assertEqual(len(result), 3)
		self.assertTrue((u"PER_BROBMA",) in result)
		self.assertTrue((u"PER_STEVEN",) in result)
		self.assertTrue((u"PER_ROBERT",) in result)
		self.assertTrue(not (u"PER_MOOOON",) in result)
		self.assertTrue(not (u"CRI_PICNIC",) in result)
		self.assertTrue(not (u"ORG_ALIENS",) in result)

	# --------------
	# query_people_without_orgs
	# --------------

	def test_query_people_without_orgs(self):
		query_people_without_orgs()

		vader = People(name="Darth Vader", idref="PER_DVADER")
		luke = People(name="Luke Skywalker", idref="PER_LUKESW")
		empire = Organizations(name="The Empire", idref="ORG_EMPIRE")
		vader.organizations.add(empire)

		vader.save()
		luke.save()
		empire.save()

		result = query_people_without_orgs()

		self.assertEqual(len(result), 1)
		self.assertTrue(not (u"PER_DVADER",) in result)
		self.assertTrue(not (u"ORG_EMPIRE",) in result)
		self.assertTrue((u"PER_LUKESW",) in result)

	# --------------
	# query_things_without_pictures
	# --------------

	def test_things_without_pictures(self):
#		query_things_without_pictures()

		obama = People(name="Barack Obama", idref="PER_BROBMA")
		me = People(name="James Kunze", idref="PER_JAMESK")
		un = Organizations(name="United Nations", idref="ORG_UNINAT")
		cachemoney = Organizations(name="Cache Money", idref="ORG_CACHEM")
		aids = Crises(name="AIDS/HIV", idref="CRI_AIDSHI")
		phasethree = Crises(name="CS373 Project Phase 3", idref="CRI_PROJCT")

		pic1 = List_Item(list_type="Images", idref="PER_BROBMA", embed="obamapic.png")
		pic2 = List_Item(list_type="Images", idref="ORG_UNINAT", embed="unpic.png")
		pic3 = List_Item(list_type="Images", idref="CRI_AIDSHI", embed="aidspic.png")

		obama.save()
		me.save()
		un.save()
		cachemoney.save()
		aids.save()
		phasethree.save()
		pic1.save()
		pic2.save()
		pic3.save()

		result = query_things_without_pictures()

		self.assertEqual(len(result), 3)
		self.assertTrue(not ("PER_BROBMA",) in result)
		self.assertTrue(not ("ORG_UNINAT",) in result)
		self.assertTrue(not ("CRI_AIDSHI",) in result)
		self.assertTrue(("PER_JAMESK",) in result)
		self.assertTrue(("ORG_CACHEM",) in result)
		self.assertTrue(("CRI_PROJCT",) in result)

	# --------------
	# query_crises_without_things
	# --------------

	def test_query_crises_without_things(self):
		query_crises_without_things()

		vader = People(name="Darth Vader", idref="PER_DVADER")
		luke = People(name="Luke Skywalker", idref="PER_LUKESW")
		empire = Organizations(name="The Empire", idref="ORG_EMPIRE")
		war = Crises(name="Intergalactic War", idref="CRI_THEWAR")
		war.people.add(vader)
		war.people.add(luke)
		war.organizations.add(empire)
		vader.organizations.add(empire)
		stormtroopers = Crises(name="Stormtroopers are dumb", idref="CRI_TROOPR")
		stormtroopers.organizations.add(empire)
		rebellion = Crises(name="The Rebellion", idref="CRI_REBELS")
		rebellion.people.add(luke)
		problem = Crises(name="The prequels suck", idref="CRI_PREQEL")
		tired = Crises(name="making these tests is tiring i'm sorry for the dumb stuff", idref="CRI_IMBORD")
		orphan = People(name="person w/o thing", idref="PER_ORPHAN")

		vader.save()
		luke.save()
		empire.save()
		war.save()
		stormtroopers.save()
		rebellion.save()
		problem.save()
		tired.save()
		orphan.save()

		result = query_crises_without_things()

		self.assertEqual(len(result), 2)
		self.assertTrue(("CRI_PREQEL",) in result)
		self.assertTrue(("CRI_IMBORD",) in result)
		self.assertTrue(not ("PER_DVADER",) in result)
		self.assertTrue(not ("PER_LUKESW",) in result)
		self.assertTrue(not ("ORG_EMPIRE",) in result)
		self.assertTrue(not ("CRI_THEWAR",) in result)
		self.assertTrue(not ("CRI_TROOPR",) in result)
		self.assertTrue(not ("CRI_REBELS",) in result)
		self.assertTrue(not ("PER_ORPHAN",) in result)

  # --------------
	# query_find_natural_disasters
	# --------------

	def test_query_find_natural_disasters(self):
		query_find_natural_disasters()
		war = Crises(name="War", idref="CRI_THEWAR")
		aliens = Crises(name="Aliens", idref="CRI_ALIENS", kind="Unnatural disaster")
		fire = Crises(name="Forest fire", idref="CRI_FFIRES", kind="Natural disaster")
		flood = Crises(name="Flooding", idref="CRI_FLOODS", kind="Natural disaster")

		war.save()
		aliens.save()
		fire.save()
		flood.save()

		result = query_find_natural_disasters()

		self.assertEqual(len(result), 2)
		self.assertTrue(("CRI_FFIRES",) in result)
		self.assertTrue(("CRI_FLOODS",) in result)
		self.assertTrue(not ("CRI_THEWAR",) in result)
		self.assertTrue(not ("CRI_ALIENS",) in result)

  # --------------
	# query_people_with_many_crises
	# --------------

	def test_query_people_with_many_crises(self):
		query_people_with_many_crises()
		zero = People(name="boring person", idref="PER_BORING")
		one = People(name="Person in one crisis", idref="PER_ONECRI")
		two = People(name="Person in two crises", idref="PER_TWOCRI")
		three = People(name="Person in three crises", idref="PER_THRCRI")
		aids = Crises(name="AIDS/HIV", idref="CRI_AIDSHI")
		fire = Crises(name="Arizona Wildfires", idref="CRI_AZWILD")
		china = Crises(name="Democracy in China", idref="CRI_CHINAD")

		aids.people.add(one)
		aids.people.add(two)
		fire.people.add(two)
		aids.people.add(three)
		fire.people.add(three)
		china.people.add(three)

		zero.save()
		one.save()
		two.save()
		three.save()
		aids.save()
		fire.save()
		china.save()

		result = query_people_with_many_crises()

		self.assertEqual(len(result), 2)
		self.assertTrue(("PER_TWOCRI",) in result)
		self.assertTrue(("PER_THRCRI",) in result)
		self.assertTrue(not ("PER_ONECRI",) in result)
		self.assertTrue(not ("PER_BORING",) in result)
		self.assertTrue(not ("CRI_AIDSHI",) in result)
		self.assertTrue(not ("CRI_AZWILD",) in result)
		self.assertTrue(not ("CRI_CHINAD",) in result)

  # --------------
	# query_orgs_with_many_videos
	# --------------

	def test_query_orgs_with_many_videos(self):
		query_orgs_with_many_videos()
		bookclub = Organizations(name="Book Club", idref="ORG_BOOKCL")
		firedept = Organizations(name="Fire Department", idref="ORG_FIREDP")
		un = Organizations(name="United Nations", idref="ORG_UNINAT")
		List_Item(list_type="Videos", idref="ORG_UNINAT").save()
		List_Item(list_type="Videos", idref="ORG_UNINAT").save()
		List_Item(list_type="Videos", idref="ORG_FIREDP").save()

		bookclub.save()
		firedept.save()
		un.save()

		result = query_orgs_with_many_videos()

		self.assertEqual(len(result), 1)
		self.assertTrue(("ORG_UNINAT",) in result)
		self.assertTrue(not ("ORG_FIREDP",) in result)
		self.assertTrue(not ("ORG_BOOKCL",) in result)

  # --------------
	# query_people_in_crises_after_millenium
	# --------------

	def test_query_people_in_crises_after_millenium(self):
		civilwar = Crises(name="The Civil War", idref="CRI_CIVWAR", date=date(1960, 1, 1))
		monday = Crises(name="Monday", idref="CRI_MONDAY", date=date(2013, 8, 5))
		lincoln = People(name="Abraham Lincoln", idref="PER_LINCLN")
		me = People(name="James Kunze", idref="PER_JAMESK")
		time = People(name="Some Time Traveler", idref="PER_TIMETR")
		fiction = People(name="Uninvolved Bystander", idref="PER_FICTIO")

		civilwar.people.add(lincoln)
		civilwar.people.add(time)
		monday.people.add(me)
		monday.people.add(time)

		civilwar.save()
		monday.save()
		lincoln.save()
		me.save()
		time.save()
		fiction.save()

		result = query_people_in_crises_after_millenium()

		self.assertEqual(len(result), 2)
		self.assertTrue(("PER_JAMESK",) in result)
		self.assertTrue(("PER_TIMETR",) in result)
		self.assertTrue(not ("PER_LINCLN",) in result)
		self.assertTrue(not ("PER_FICTIO",) in result)
		self.assertTrue(not ("CRI_CIVWAR",) in result)
		self.assertTrue(not ("CRI_MONDAY",) in result)


  # --------------
	# query_people_with_red_cross_videos
	# --------------

	def test_query_people_with_red_cross_videos(self):
		redcross = Organizations(name="The Red Cross", idref="ORG_REDCRS")
		firedp = Organizations(name="Fire Department", idref="ORG_FIREDP")
		dracula = People(name="Dracula", idref="PER_DRACUL")
		fireman = People(name="Fireman", idref="PER_FIREMN")
		multitasker = People(name="Multitasker", idref="PER_MULTAS")
		joshmo = People(name="John Smith", idref="PER_BORING")
		lincoln = People(name="Abraham Lincoln", idref="PER_LINCLN")

		List_Item(list_type="Videos", idref="PER_DRACUL").save()
		List_Item(list_type="Videos", idref="PER_MULTAS").save()
		List_Item(list_type="Videos", idref="PER_LINCLN").save()

		dracula.organizations.add(redcross)
		fireman.organizations.add(firedp)
		multitasker.organizations.add(redcross)
		multitasker.organizations.add(firedp)

		redcross.save()
		firedp.save()
		dracula.save()
		fireman.save()
		multitasker.save()
		lincoln.save()

		result = query_people_with_red_cross_videos()

		self.assertEqual(len(result), 2)
		self.assertTrue(("PER_DRACUL",) in result)
		self.assertTrue(("PER_MULTAS",) in result)
		self.assertTrue(not ("PER_LINCLN",) in result)
		self.assertTrue(not ("PER_BORING",) in result)
		self.assertTrue(not ("PER_FIREMN",) in result)
		self.assertTrue(not ("ORG_REDCRS",) in result)
		self.assertTrue(not ("PER_FIREDP",) in result)


	# --------------
	# query_number_images_before_millenium
	# --------------

	def test_query_number_images_before_millenium(self):
		fire = Crises(name="Arizona Wildfires", idref="CRI_AZWILD", date=date(2013, 8, 5))
		china = Crises(name="Democracy in China", idref="CRI_CHINAD", date=date(2013, 8, 5))
		civilwar = Crises(name="The Civil War", idref="CRI_CIVWAR", date=date(1960, 1, 1))
		dracula = People(name="Dracula", idref="PER_DRACUL")

		fire.save()
		china.save()
		civilwar.save()

		List_Item(idref="CRI_AZWILD", list_type="Images").save()
		List_Item(idref="CRI_CHINAD", list_type="Images").save()
		List_Item(idref="CRI_CHINAD", list_type="Videos").save()
		List_Item(idref="CRI_CHINAD", list_type="Maps").save()
		List_Item(idref="CRI_CIVWAR", list_type="Images").save()
		List_Item(idref="CRI_CIVWAR", list_type="Images").save()
		List_Item(idref="CRI_CIVWAR", list_type="Maps").save()
		List_Item(idref="PER_DRACUL", list_type="Images").save()
		List_Item(idref="PER_DRACUL", list_type="Videos").save()

		result = query_number_images_before_millenium()

		self.assertEqual(len(result), 1)
		self.assertTrue((2,) in result)

	# --------------
	# xml_merge
	# --------------

	def test_xml_merge_entitycount(self):
		Crises.objects.all().delete()
		People.objects.all().delete()
		Organizations.objects.all().delete()
		List_Item.objects.all().delete()

		xml_file         = open('wcdb/WCDB2.xml', 'r')
		xml_file_tomerge = open('wcdb/crisix.xml', 'r')
        	xsd = open("wcdb/WCDB2.xsd.xml", 'r')

		et = xml_reader(xml_file, xsd)
		xml_etree2mods(et.getroot())

		incoming_data = xml_reader(xml_file_tomerge, xsd)
		xml_etree2mods(incoming_data.getroot())
		# now is when you want to know how many videos there are in the database
		
		root = xml_mods2etree().getroot()

		crisis_cnt = 0
		person_cnt = 0
		org_cnt    = 0

		for child in list(root) :
			if child.tag == "Crisis" :
				crisis_cnt += 1
			elif child.tag == "Organization" :
				org_cnt += 1
			elif child.tag == "Person" :
				person_cnt += 1

		self.assertEqual(crisis_cnt, 19)
		self.assertEqual(person_cnt, 19)
		self.assertEqual(org_cnt, 20)

	def test_query_people_without_orgs(self):
		query_people_without_orgs()

		vader = People(name="Darth Vader", idref="PER_DVADER")
		luke = People(name="Luke Skywalker", idref="PER_LUKESW")
		empire = Organizations(name="The Empire", idref="ORG_EMPIRE")
		vader.organizations.add(empire)

		vader.save()
		luke.save()
		empire.save()

		result = query_people_without_orgs()

		self.assertEqual(len(result), 1)
		self.assertTrue(not (u"PER_DVADER",) in result)
		self.assertTrue(not (u"ORG_EMPIRE",) in result)
		self.assertTrue((u"PER_LUKESW",) in result)

	# --------------
	# query_things_without_pictures
	# --------------

	def test_query_things_without_pictures(self):
		query_things_without_pictures()

		obama = People(name="Barack Obama", idref="PER_BROBMA")
		me = People(name="James Kunze", idref="PER_JAMESK")
		un = Organizations(name="United Nations", idref="ORG_UNINAT")
		cachemoney = Organizations(name="Cache Money", idref="ORG_CACHEM")
		aids = Crises(name="AIDS/HIV", idref="CRI_AIDSHI")
		phasethree = Crises(name="CS373 Project Phase 3", idref="CRI_PROJCT")

		pic1 = List_Item(list_type="Images", idref="PER_BROBMA", embed="obamapic.png")
		pic2 = List_Item(list_type="Images", idref="ORG_UNINAT", embed="unpic.png")
		pic3 = List_Item(list_type="Images", idref="CRI_AIDSHI", embed="aidspic.png")

		obama.save()
		me.save()
		un.save()
		cachemoney.save()
		aids.save()
		phasethree.save()
		pic1.save()
		pic2.save()
		pic3.save()

		result = query_things_without_pictures()

		self.assertEqual(len(result), 3)
		self.assertTrue(not ("PER_BROBMA",) in result)
		self.assertTrue(not ("ORG_UNINAT",) in result)
		self.assertTrue(not ("CRI_AIDSHI",) in result)
		self.assertTrue(("PER_JAMESK",) in result)
		self.assertTrue(("ORG_CACHEM",) in result)
		self.assertTrue(("CRI_PROJCT",) in result)

	# --------------
	# query_crises_without_things
	# --------------

	def test_query_crises_without_things(self):
		query_crises_without_things()

		vader = People(name="Darth Vader", idref="PER_DVADER")
		luke = People(name="Luke Skywalker", idref="PER_LUKESW")
		empire = Organizations(name="The Empire", idref="ORG_EMPIRE")
		war = Crises(name="Intergalactic War", idref="CRI_THEWAR")
		war.people.add(vader)
		war.people.add(luke)
		war.organizations.add(empire)
		vader.organizations.add(empire)
		stormtroopers = Crises(name="Stormtroopers are dumb", idref="CRI_TROOPR")
		stormtroopers.organizations.add(empire)
		rebellion = Crises(name="The Rebellion", idref="CRI_REBELS")
		rebellion.people.add(luke)
		problem = Crises(name="The prequels suck", idref="CRI_PREQEL")
		tired = Crises(name="making these tests is tiring i'm sorry for the dumb stuff", idref="CRI_IMBORD")
		orphan = People(name="person w/o thing", idref="PER_ORPHAN")

		vader.save()
		luke.save()
		empire.save()
		war.save()
		stormtroopers.save()
		rebellion.save()
		problem.save()
		tired.save()
		orphan.save()

		result = query_crises_without_things()

		self.assertEqual(len(result), 2)
		self.assertTrue(("CRI_PREQEL",) in result)
		self.assertTrue(("CRI_IMBORD",) in result)
		self.assertTrue(not ("PER_DVADER",) in result)
		self.assertTrue(not ("PER_LUKESW",) in result)
		self.assertTrue(not ("ORG_EMPIRE",) in result)
		self.assertTrue(not ("CRI_THEWAR",) in result)
		self.assertTrue(not ("CRI_TROOPR",) in result)
		self.assertTrue(not ("CRI_REBELS",) in result)
		self.assertTrue(not ("PER_ORPHAN",) in result)

  # --------------
	# query_find_natural_disasters
	# --------------

	def test_query_find_natural_disasters(self):
		query_find_natural_disasters()
		war = Crises(name="War", idref="CRI_THEWAR")
		aliens = Crises(name="Aliens", idref="CRI_ALIENS", kind="Unnatural disaster")
		fire = Crises(name="Forest fire", idref="CRI_FFIRES", kind="Natural disaster")
		flood = Crises(name="Flooding", idref="CRI_FLOODS", kind="Natural disaster")

		war.save()
		aliens.save()
		fire.save()
		flood.save()

		result = query_find_natural_disasters()

		self.assertEqual(len(result), 2)
		self.assertTrue(("CRI_FFIRES",) in result)
		self.assertTrue(("CRI_FLOODS",) in result)
		self.assertTrue(not ("CRI_THEWAR",) in result)
		self.assertTrue(not ("CRI_ALIENS",) in result)

  # --------------
	# query_people_with_many_crises
	# --------------

	def test_query_people_with_many_crises(self):
		query_people_with_many_crises()
		zero = People(name="boring person", idref="PER_BORING")
		one = People(name="Person in one crisis", idref="PER_ONECRI")
		two = People(name="Person in two crises", idref="PER_TWOCRI")
		three = People(name="Person in three crises", idref="PER_THRCRI")
		aids = Crises(name="AIDS/HIV", idref="CRI_AIDSHI")
		fire = Crises(name="Arizona Wildfires", idref="CRI_AZWILD")
		china = Crises(name="Democracy in China", idref="CRI_CHINAD")

		aids.people.add(one)
		aids.people.add(two)
		fire.people.add(two)
		aids.people.add(three)
		fire.people.add(three)
		china.people.add(three)

		zero.save()
		one.save()
		two.save()
		three.save()
		aids.save()
		fire.save()
		china.save()

		result = query_people_with_many_crises()

		self.assertEqual(len(result), 2)
		self.assertTrue(("PER_TWOCRI",) in result)
		self.assertTrue(("PER_THRCRI",) in result)
		self.assertTrue(not ("PER_ONECRI",) in result)
		self.assertTrue(not ("PER_BORING",) in result)
		self.assertTrue(not ("CRI_AIDSHI",) in result)
		self.assertTrue(not ("CRI_AZWILD",) in result)
		self.assertTrue(not ("CRI_CHINAD",) in result)

  # --------------
	# query_orgs_with_many_videos
	# --------------

	def test_query_orgs_with_many_videos(self):
		query_orgs_with_many_videos()
		bookclub = Organizations(name="Book Club", idref="ORG_BOOKCL")
		firedept = Organizations(name="Fire Department", idref="ORG_FIREDP")
		un = Organizations(name="United Nations", idref="ORG_UNINAT")
		List_Item(list_type="Videos", idref="ORG_UNINAT").save()
		List_Item(list_type="Videos", idref="ORG_UNINAT").save()
		List_Item(list_type="Videos", idref="ORG_FIREDP").save()

		bookclub.save()
		firedept.save()
		un.save()

		result = query_orgs_with_many_videos()

		self.assertEqual(len(result), 1)
		self.assertTrue(("ORG_UNINAT",) in result)
		self.assertTrue(not ("ORG_FIREDP",) in result)
		self.assertTrue(not ("ORG_BOOKCL",) in result)

  # --------------
	# query_people_in_crises_after_millenium
	# --------------

	def test_query_people_in_crises_after_millenium(self):
		civilwar = Crises(name="The Civil War", idref="CRI_CIVWAR", date=date(1960, 1, 1))
		monday = Crises(name="Monday", idref="CRI_MONDAY", date=date(2013, 8, 5))
		lincoln = People(name="Abraham Lincoln", idref="PER_LINCLN")
		me = People(name="James Kunze", idref="PER_JAMESK")
		time = People(name="Some Time Traveler", idref="PER_TIMETR")
		fiction = People(name="Uninvolved Bystander", idref="PER_FICTIO")

		civilwar.people.add(lincoln)
		civilwar.people.add(time)
		monday.people.add(me)
		monday.people.add(time)

		civilwar.save()
		monday.save()
		lincoln.save()
		me.save()
		time.save()
		fiction.save()

		result = query_people_in_crises_after_millenium()

		self.assertEqual(len(result), 2)
		self.assertTrue(("PER_JAMESK",) in result)
		self.assertTrue(("PER_TIMETR",) in result)
		self.assertTrue(not ("PER_LINCLN",) in result)
		self.assertTrue(not ("PER_FICTIO",) in result)
		self.assertTrue(not ("CRI_CIVWAR",) in result)
		self.assertTrue(not ("CRI_MONDAY",) in result)


  # --------------
	# query_people_with_red_cross_videos
	# --------------

	def test_query_people_with_red_cross_videos(self):
		redcross = Organizations(name="The Red Cross", idref="ORG_REDCRS")
		firedp = Organizations(name="Fire Department", idref="ORG_FIREDP")
		dracula = People(name="Dracula", idref="PER_DRACUL")
		fireman = People(name="Fireman", idref="PER_FIREMN")
		multitasker = People(name="Multitasker", idref="PER_MULTAS")
		joshmo = People(name="John Smith", idref="PER_BORING")
		lincoln = People(name="Abraham Lincoln", idref="PER_LINCLN")

		List_Item(list_type="Videos", idref="PER_DRACUL").save()
		List_Item(list_type="Videos", idref="PER_MULTAS").save()
		List_Item(list_type="Videos", idref="PER_LINCLN").save()

		dracula.organizations.add(redcross)
		fireman.organizations.add(firedp)
		multitasker.organizations.add(redcross)
		multitasker.organizations.add(firedp)

		redcross.save()
		firedp.save()
		dracula.save()
		fireman.save()
		multitasker.save()
		lincoln.save()

		result = query_people_with_red_cross_videos()

		self.assertEqual(len(result), 2)
		self.assertTrue(("PER_DRACUL",) in result)
		self.assertTrue(("PER_MULTAS",) in result)
		self.assertTrue(not ("PER_LINCLN",) in result)
		self.assertTrue(not ("PER_BORING",) in result)
		self.assertTrue(not ("PER_FIREMN",) in result)
		self.assertTrue(not ("ORG_REDCRS",) in result)
		self.assertTrue(not ("PER_FIREDP",) in result)


	# --------------
	# query_number_images_before_millenium
	# --------------

	def test_query_number_images_before_millenium(self):
		fire = Crises(name="Arizona Wildfires", idref="CRI_AZWILD", date=date(2013, 8, 5))
		china = Crises(name="Democracy in China", idref="CRI_CHINAD", date=date(2013, 8, 5))
		civilwar = Crises(name="The Civil War", idref="CRI_CIVWAR", date=date(1960, 1, 1))
		dracula = People(name="Dracula", idref="PER_DRACUL")

		fire.save()
		china.save()
		civilwar.save()

		List_Item(idref="CRI_AZWILD", list_type="Images").save()
		List_Item(idref="CRI_CHINAD", list_type="Images").save()
		List_Item(idref="CRI_CHINAD", list_type="Videos").save()
		List_Item(idref="CRI_CHINAD", list_type="Maps").save()
		List_Item(idref="CRI_CIVWAR", list_type="Images").save()
		List_Item(idref="CRI_CIVWAR", list_type="Images").save()
		List_Item(idref="CRI_CIVWAR", list_type="Maps").save()
		List_Item(idref="PER_DRACUL", list_type="Images").save()
		List_Item(idref="PER_DRACUL", list_type="Videos").save()

		result = query_number_images_before_millenium()

		self.assertEqual(len(result), 1)
		self.assertTrue((2,) in result)

	# --------------
	# search_one_word
	# --------------

	def test_search_one_word(self):
		fire = Crises(name="Arizona Wildfires", idref="CRI_AZWILD", date=date(2013, 8, 5))
		china = Crises(name="Democracy in China", idref="CRI_CHINAD", date=date(2013, 8, 5))
		civilwar = Crises(name="The Civil War", idref="CRI_CIVWAR", date=date(1960, 1, 1))
		dracula = People(name="Dracula", idref="PER_DRACUL")
		firedp = Organizations(name="Arizona Fire Department", idref="ORG_FIREDP")

		fire.save()
		china.save()
		civilwar.save()
		dracula.save()
		firedp.save()

		self.assertEqual(search_one_word('Arizona', []), [("CRI_AZWILD", "Arizona Wildfires", "Arizona Wildfires"), ("ORG_FIREDP", "Arizona Fire Department", "Arizona Fire Department")])
		self.assertEqual(search_one_word('Fire', []), [("CRI_AZWILD", "Arizona Wildfires", "Arizona Wildfires"), ("ORG_FIREDP", "Arizona Fire Department", "Arizona Fire Department")])
		self.assertEqual(search_one_word('Extreme Elevator Riding', []), [])
		self.assertEqual(search_one_word('Dracula', []), [("PER_DRACUL", "Dracula", "Dracula")])
		self.assertEqual(search_one_word('Fire', ["CRI_AZWILD"]), [("ORG_FIREDP", "Arizona Fire Department", "Arizona Fire Department")])
		self.assertEqual(search_one_word('Fire', ["ORG_FIREDP"]), [("CRI_AZWILD", "Arizona Wildfires", "Arizona Wildfires")])
		self.assertEqual(search_one_word('Fire', ["CRI_AZWILD", "ORG_FIREDP"]), [])
		self.assertEqual(search_one_word('Democracy in China', []), search_one_word('DeMoCrAcY In CHINA', []))
