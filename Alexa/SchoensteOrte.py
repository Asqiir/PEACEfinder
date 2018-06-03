import sys

stadtteil = sys.argv[1]

zuordnung = {
"Südstadt":["der Kringelgraben", "Biestow", "die Mensa"],
"KTV":["der Lindenpark", "der Ulmencampus"],
"Komponistenviertel":["der Botanische Garten", "der Schwanenteich"],
"Warnemünde":["der Kurpark", "der Stephan-Jantzen-Park", "die Seepromenade", "der Strand"]
}

orte = zuordnung.get(stadtteil)
if orte == None:
	print ("Leider habe ich deinen Ort nicht gefunden, probiere es doch mit einem anderen.")
else:
	auflistung = ""
	for i in range (0,len(orte)):
		ist_erster_ort = (i==0)
		ist_letzter_ort = (i==len(orte)-1)
		if ist_erster_ort:
			auflistung = auflistung + ""
		if not ist_erster_ort  and not ist_letzter_ort:
			auflistung = auflistung + ", "
		if ist_letzter_ort:
			auflistung = auflistung + " und "
			
		auflistung = auflistung + orte[i]
	
	
	
	print ("Die schönsten Orte im Stadtteil "+ stadtteil +" sind " + auflistung + ".")


