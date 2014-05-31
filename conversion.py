#Source: http://hannahfry.co.uk/2011/10/10/converting-british-national-grid-to-latitude-and-longitude/

from scipy import *
# import csv

def OSGB36toWGS84(E,N):

    #E, N are the British national grid coordinates - eastings and northings
    a, b = 6377563.396, 6356256.909     #The Airy 180 semi-major and semi-minor axes used for OSGB36 (m)
    F0 = 0.9996012717                   #scale factor on the central meridian
    lat0 = 49*pi/180                    #Latitude of true origin (radians)
    lon0 = -2*pi/180                    #Longtitude of true origin and central meridian (radians)
    N0, E0 = -100000, 400000            #Northing & easting of true origin (m)
    e2 = 1 - (b*b)/(a*a)                #eccentricity squared
    n = (a-b)/(a+b)

    #Initialise the iterative variables
    lat,M = lat0, 0

    while N-N0-M >= 0.00001: #Accurate to 0.01mm
        lat = (N-N0-M)/(a*F0) + lat;
        M1 = (1 + n + (5/4)*n**2 + (5/4)*n**3) * (lat-lat0)
        M2 = (3*n + 3*n**2 + (21/8)*n**3) * sin(lat-lat0) * cos(lat+lat0)
        M3 = ((15/8)*n**2 + (15/8)*n**3) * sin(2*(lat-lat0)) * cos(2*(lat+lat0))
        M4 = (35/24)*n**3 * sin(3*(lat-lat0)) * cos(3*(lat+lat0))
        #meridional arc
        M = b * F0 * (M1 - M2 + M3 - M4)          

    #transverse radius of curvature
    nu = a*F0/sqrt(1-e2*sin(lat)**2)
    #meridional radius of curvature
    rho = a*F0*(1-e2)*(1-e2*sin(lat)**2)**(-1.5)
    eta2 = nu/rho-1

    secLat = 1./cos(lat)
    VII = tan(lat)/(2*rho*nu)
    VIII = tan(lat)/(24*rho*nu**3)*(5+3*tan(lat)**2+eta2-9*tan(lat)**2*eta2)
    IX = tan(lat)/(720*rho*nu**5)*(61+90*tan(lat)**2+45*tan(lat)**4)
    X = secLat/nu
    XI = secLat/(6*nu**3)*(nu/rho+2*tan(lat)**2)
    XII = secLat/(120*nu**5)*(5+28*tan(lat)**2+24*tan(lat)**4)
    XIIA = secLat/(5040*nu**7)*(61+662*tan(lat)**2+1320*tan(lat)**4+720*tan(lat)**6)
    dE = E-E0

    lat = lat - VII*dE**2 + VIII*dE**4 - IX*dE**6
    lon = lon0 + X*dE - XI*dE**3 + XII*dE**5 - XIIA*dE**7

    #Convert to degrees
    lat = lat*180/pi
    lon = lon*180/pi

    return [lon, lat]

#Read in from a file
# BNG = csv.reader(open('BNG.csv', 'rU'), delimiter = ',')
# BNG.next()

# #Get the output file ready
# outputFile = open('BNGandLatLon.csv', 'wb')
# output=csv.writer(outputFile,delimiter=',')
# output.writerow(['Lat', 'Lon', 'E', 'N'])

# #Loop through the data
# for E,N in BNG:
#     lat, lon = OSGB36toWGS84(float(E), float(N))
#     output.writerow([str(lat), str(lon), str(E), str(N)])
# #Close the output file
# outputFile.close()