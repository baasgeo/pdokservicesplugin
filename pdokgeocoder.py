import json
import os
import urllib
import urllib2
from xml.dom.minidom import parse

searchstring = 'riouwstaat, haarlem'
#searchstring = 'kenaustraat 12, haarlem'
#searchstring = 'amperestraat, den bosch'
searchstring = 'kenaustraat, haarlem'
searchstring = 'riouwstraat 23'
#searchstring = 'Riouwstraat 1 Haarlem Noord-Holland'
#searchstring = ''
#searchstring = 'utrecht'
#searchstring = 'kerkstraat 1'
#searchstring = 'veld 1'
#searchstring = 'valkenburg' # geeft 0 hits en valkeburg heeft de juiste??
#searchstring = 'noordwijk'
#searchstring = '2022ZJ'
#searchstring = '2022ZJ 23'

def search(searchstring):
    """

    :param searchstring:
    """
    # be carefull NO spaces in it: urllib2 will think these are two urls and choke
    url = "http://geodata.nationaalgeoregister.nl/geocoder/Geocoder?zoekterm=" + urllib.quote_plus(searchstring)
    #url = "http://www.geocoders.nl/places?format=xml&address=" + urllib.quote_plus(searchstring)
    #print url
    addressesarray = []
    try:
        response = urllib.urlopen(url)
        if response.code != 200:
            print 'ERROR %s' % response.code
            exit()
        doc = parse(response)

        addresses = doc.getElementsByTagName("xls:GeocodedAddress")
        for address in addresses:
            street = u""
            building = u""
            streetAddress = address.getElementsByTagName("xls:StreetAddress")
            if len(streetAddress)>0:
                streetAddress = streetAddress[0]
                street = streetAddress.getElementsByTagName("xls:Street")
                if len(street)>0:
                    street = street[0].firstChild.nodeValue
                else:
                    street = u""
                building = streetAddress.getElementsByTagName("xls:Building")
                if len(building)>0:
                    building = building[0]
                    number = building.getAttribute("number")
                    subdivision = building.getAttribute("subdivision")
                    building = number+subdivision
                else:
                    building = u""
            postalcode = address.getElementsByTagName("xls:PostalCode")
            if len(postalcode)>0:
                postalcode = postalcode[0].firstChild.nodeValue
            else:
                postalcode = u""
            plaats = u""
            gemeente = u""
            provincie = u""
            places = address.getElementsByTagName("xls:Place")
            for place in places:
                if place.getAttribute("type")=="CountrySubdivision":
                    prov = place.firstChild.nodeValue
                if place.getAttribute("type")=="Municipality":
                    gemeente = place.firstChild.nodeValue
                if place.getAttribute("type")=="MunicipalitySubdivision":
                    plaats = place.firstChild.nodeValue
            pos = address.getElementsByTagName("gml:pos")[0].firstChild.nodeValue
            # if total_address is correctly written xmlTag exists:
            if pos:
                remark=True
                # split X and Y coordinate in list
                XY = pos.split()
                if XY:
                    x = float(XY[0])
                    y = float(XY[1])
                    #print "point: " + str(x) + ", " + str(y)
            adres = ""
            if len(street)>0:
                # sometimes we only get gemeente
                plaatsgemeente = plaats
                if len(plaatsgemeente)==0:
                    plaatsgemeente = gemeente
                if len(building)>0:
                    adres = 'adres: ' + (street + " " + building + " " + postalcode + " " + plaatsgemeente + " " + prov).replace('  ',' ')
                else:
                    adres = 'straat: ' + (street + " " + building + " " + postalcode  + " " + plaatsgemeente + " " + prov).replace('  ',' ')
            elif len(plaats)>0:
                adres = 'plaats: '+ (plaats + " (" + gemeente + ") in " + prov).replace('  ',' ')
            elif len(gemeente)>0:
                adres = 'gemeente: ' +(gemeente + " in " + prov).replace('  ',' ')
            elif len(prov)>0:
                adres = 'provincie: ' + prov
            #print adres.strip().replace('  ',' ') + ' ('+str(x) + ", " + str(y)+')'
            addressdict = {
                'straat':street,
                'adres':building,
                'postcode':postalcode,
                'plaats':plaats,
                'gemeente':gemeente,
                'provincie':prov,
                'x':x,
                'y':y,
                'adrestekst': adres.strip().replace('  ',' ')
            }
            addressesarray.append(addressdict)
    except Exception, e:
        print e
    return addressesarray

if __name__ == "__main__":
    search(searchstring)