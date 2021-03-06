"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import linkedlistiterator as it
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'dateIndex': None,
                'hourIndex':None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer["hourIndex"] = om.newMap(omaptype='RBT',
                                      comparefunction=compareHour)
    return analyzer


# Funciones para agregar informacion al catalogo

def addAccident(analyzer, accident):
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    updateHourIndex(analyzer['hourIndex'], accident)
    return analyzer

def updateHourIndex(map, accident):
    horaaccidente = accident['Start_Time']
    accidenthour = datetime.datetime.strptime(horaaccidente, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidenthour.time())
    if entry is None:
        datentry = newHourEntry(accident)
        om.put(map, accidenthour.time(), datentry)
    else:
        datentry = me.getValue(entry)
    addhour(datentry, accident)
    return map

def newHourEntry(accident):
    entry = {'listaccidentes': None}
    entry['listaccidentes'] = lt.newList('SINGLE_LINKED', compareHour)
    return entry

def addhour(datentry, accident):
    lst = datentry['listaccidentes']
    lt.addLast(lst, accident)
    return datentry

def updateDateIndex(map, accident):
    occurreddate = accident['Start_Time']
    accidentdata = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdata.date())
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, accidentdata.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)
    return map

def addDateIndex(datentry, accident):
    lst = datentry['lstaccidents']
    lt.addLast(lst, accident)
    Seveindex = datentry['SeverityIndex']
    seventry = m.get(Seveindex, accident['Severity'])
    if (seventry is None):
        entry = newSeverityEntry(accident['Severity'], accident)
        lt.addLast(entry['lstSeverities'], accident)
        m.put(Seveindex, accident['Severity'], entry)
    else:
        entry = me.getValue(seventry)
        lt.addLast(entry['lstSeverities'], accident)
    return datentry


def newDataEntry(accident):
    entry = {'SeverityIndex': None, 'lstaccidents': None}
    entry['SeverityIndex'] = m.newMap(numelements=61,
                                     maptype='PROBING',
                                     comparefunction=compareSeverity)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


def newSeverityEntry(entrada1, accident):
    sepentry = {'severity': None, 'lstSeverities': None}
    sepentry['severity'] = entrada1
    sepentry['lstSeverities'] = lt.newList('SINGLELINKED', compareSeverity)
    return sepentry


# ==============================
# Funciones de consulta
# ==============================


def accidentsSize(analyzer):
    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    return om.maxKey(analyzer['dateIndex'])


def getAccidentsByRange(analyzer, initialDate, finalDate):
    lst = om.values(analyzer['dateIndex'], initialDate.date(), finalDate.date())
    return lst


def getAccidentsByRangeSeverity(analyzer, initialDate, severitycode):
    axidate = om.get(analyzer['dateIndex'], initialDate)
    if axidate['key'] is not None:
        severitymap = me.getValue(axidate)['SeverityIndex']
        numseverities = m.get(severitymap, severitycode)
        if numseverities is not None:
            return m.size(me.getValue(numseverities)['lstSeverities'])
        return 0 

def hallar_muyrepetido(lst):
    lista=[]
    iterator = it.newIterator(lst)
    while it.hasNext(iterator):
        itet=it.next(iterator)
        iterator2 = it.newIterator(itet["lstaccidents"])
        while it.hasNext(iterator2):
            itet2=it.next(iterator2)
            fechahora=datetime.datetime.strptime(itet2["Start_Time"], '%Y-%m-%d %H:%M:%S')
            lista.append(fechahora.date())      
    maxi = 0
    ret=None
    for cada_fecha in lista:
        cant=lista.count(cada_fecha)
        if cant > maxi:
            maxi = cant
            ret=cada_fecha
    return (ret,maxi)

#datetime.datetime.strptime(itet2["Start_Time"], '%Y-%m-%d'   --- hora '%Y-%m-%d %H:%M:%S')
#datetime.datetime.hour(fecha completa, '%H:%M:%S')  

def hallar_categoria(lst):
    lista=[]
    iterator = it.newIterator(lst)
    while it.hasNext(iterator):
        itet=it.next(iterator)
        iterator2 = it.newIterator(itet["lstaccidents"])
        while it.hasNext(iterator2):
            itet2=it.next(iterator2)
            lista.append(itet2["Severity"])
    maxi = 0
    ret=None
    for severidad in lista:
        cant=lista.count(severidad)
        if cant > maxi:
            maxi = cant
            ret=severidad
    return (ret,maxi)


def getStateInRange(lst):
    lista=[]
    iterator = it.newIterator(lst)
    while it.hasNext(iterator):
        itet=it.next(iterator)
        iterator2 = it.newIterator(itet["lstaccidents"])
        while it.hasNext(iterator2):
            itet2=it.next(iterator2)
            lista.append(itet2["State"])
    maxi = 0
    ret=None
    for estado in lista:
        cant=lista.count(estado)
        if cant > maxi:
            maxi = cant
            ret=estado
    return (ret,maxi)

def ObtenerAccidentesPorHora(lst):
    lista=[]
    dik={"Severidad1":0,"Severidad2":0,"Severidad3":0,"Severidad4":0}
    m=0
    iterator = it.newIterator(lst)
    while it.hasNext(iterator):
        itet=it.next(iterator)
        tamanor=lt.size(itet["listaccidentes"])
        i=0
        while i!=tamanor:
            iterator3=it.newIterator(itet["listaccidentes"])
            while it.hasNext(iterator3):
                itat=it.next(iterator3)
                if int(itat["Severity"])==1:
                    dik["Severidad1"]=dik["Severidad1"]+1
                elif int(itat["Severity"])==2:
                    dik["Severidad2"]=dik["Severidad2"]+1
                elif int(itat["Severity"])==3:
                    dik["Severidad3"]=dik["Severidad3"]+1
                elif int(itat["Severity"])==4:
                    dik["Severidad4"]=dik["Severidad4"]+1
            i+=1
        m=m+i
    lista.append(m)
    if m!=0:
        porcentajesev1=round(((dik["Severidad1"]/m)*100),2)
        porcentajesev2=round(((dik["Severidad2"]/m)*100),2)
        porcentajesev3=round(((dik["Severidad3"]/m)*100),2)
        porcentajesev4=round(((dik["Severidad4"]/m)*100),2)
    lista.append(porcentajesev1)
    lista.append(porcentajesev2)
    lista.append(porcentajesev3)
    lista.append(porcentajesev4)
    return (lista,dik)

def getAccidentsByRangeHora(analyzer, initialDate, finalDate):
    lst = om.values(analyzer['hourIndex'], initialDate.time(), finalDate.time())
    return lst

# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareHour(hour1, hour2):
    if (hour1 == hour2):
        return 0
    elif (hour1 > hour2):
        return 1
    else:
        return -1


def compareSeverity(severity1, severity2):
    seve = me.getKey(severity2)
    if (severity1 == seve):
        return 0
    elif (severity1 > seve):
        return 1
    else:
        return -1

def ajustarhora(hora):
    "(HH-MM-SS)"
    #fecha_str = "14/07/2014"
    #date_object = datetime.strptime(fecha_str, '%H:%M:%S')
    #fecha_str = datetime.strftime(date_object, '%H:%M:%S'')
    m1=hora[3]
    m2=hora[4]
    h1=hora[0]
    h2=hora[1]
    HH=h1+h2
    MM=m1+m2
    if int(HH)==23 and int(MM)==59:
        ret=hora
    elif int(MM) < 30 and int(MM) >= 1:
        ret=hora.replace(MM,"30")
    elif int(MM) > 30:
        h2 = int(h2)+1
        ret=hora.replace(HH,h1+str(h2)).replace(MM,"00")
    elif int(MM) > 30 and int(HH)==23:
        ret=hora.replace(MM,"00").replace(HH,"00")
    return ret