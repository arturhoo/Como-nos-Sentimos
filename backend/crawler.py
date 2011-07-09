#coding: utf-8

from twython import Twython
import re
import MySQLdb
import sys

try:
    from crawler_local_settings import *
except ImportError:
    sys.exit("No Crawler Local Settings found!")

def carregaDicio (dbCursor):
    ''' Carrega dicionario de sentimentos a partir
    do banco de dados'''
    dbCursor.execute(''' select re, id from feelings''')
    dicionario = {}
    for row in dbCursor:
        dicionario[r"\b"+row[0].encode('utf-8')] = row[1]

    return dicionario

def insereTweet(dbCursor, result, sentimento, date_time):
    ''' Insere tweet no banco de dados'''
    texto = re.sub('\n', ' ', result['text'])
    t = (   result['id'], \
            result['from_user'], \
            texto, \
            sentimento, \
            date_time[0], \
            date_time[1])
    try:
        dbCursor.execute('''insert into tweets
        values (%s, %s, %s, %s, %s, %s)''', t)

    except Exception, err:
        # print 'NAO INSERI TWEET: ', err
        conn.rollback()
        return 0

    else:
        print result['text']
        return 1

def insereUsuario(dbCursor, result):
    t = (result['from_user'],)
    try:
        dbCursor.execute('''insert into users
        values (%s, NULL, NULL, NULL, NULL, NULL, 0)''', t)

    except Exception, err:
        #print 'NAO INSERI USER: ', err
        conn.rollback()

def retornaUltimoTweet(dbCursor):
    '''Retorna id do tweet mais recente'''
    dbCursor.execute('''select max(id) from access''')
    for row in dbCursor:
        return row[0]

def gravaUltimoTweet(dbCursor, results):
    '''Grava ultimo tweet processado'''
    t = (results[0][0]['id'],)

    dbCursor.execute('''insert into access
    values (%s)''', t)

def populaUsuarios(dbCursor, twythonOb, inseridos):
    lenght = len(inseridos)
    index = 0

    # Twitter so permite 100 buscas de usuario por vez
    while index < lenght:
        query = ''
        # Monta a query
        for pages in range(0, 99):
            if index >= lenght:
                break
            query += str(inseridos[index]['from_user'])
            query += ','
            index += 1

        print query
        results = twythonOb.bulkUserLookup(screen_name = query)
        for result in results:
            t = (   result['name'], \
                    result['location'], \
                    result['description'], \
                    result['screen_name'],)
            try:
                dbCursor.execute('''update users
                set name=%s, location=%s, description=%s
                where screen_name=%s''', t)

            except Exception, err:
                print 'ERROR: ', err
                conn.rollback()


def defineSentimento(dicio, texto, rePrefixo):
    '''Define sentimento a partir do texto'''
    for k, v in dicio.items():
        if re.search(rePrefixo+k, texto.encode('utf-8'), re.IGNORECASE):
            return v

    return 0

def processaData(date_time):
    months = {  'Jan':'01','Feb':'02','Mar':'03','Apr':'04', \
                'May':'05','Jun':'06','Jul':'07','Aug':'08', \
                'Sep':'07','Oct':'10','Nov':'11','Dec':'12'}

    t = re.split(',{0,1} ', date_time)
    date = t[3] + '-' + months[t[2]] + '-' + t[1]
    time = t[4]

    return (date, time)



########################################################################

# Abrindo banco de dados MySQL
conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, charset='utf8', use_unicode=True, init_command='SET NAMES utf8')
print conn.character_set_name()
c = conn.cursor()
f = open('garbage', 'w')


# Carrega dicionario de sentimentos
dicio = carregaDicio(c)

# Retorna ultimo tweet
ultimo = retornaUltimoTweet(c)

# Puxa tweets
twitter = Twython(  twitter_token = CONSUMER_KEY, \
                    twitter_secret = CONSUMER_SECRET, \
                    oauth_token = TOKEN_KEY, \
                    oauth_token_secret = TOKEN_SECRET)

all_results = []
all_inseridos = []
count = 0

for page in range(1, 100):
    results = twitter.searchTwitter(q='''"eu to" OR "me sentindo" OR "estou"''', \
                                    rpp='15', \
                                    page=str(page), \
                                    since_id=str(ultimo), \
                                    result_type='recent')['results']
    if not results:
        break
    all_results.append(results)
    rePrefixo = "^(?!RT).*(eu t(o|ô)|estou|me sentindo).*(?!n(a|ã)o).*"

    # Para cada um dos resultados da busca
    for result in results:
        sentimento_id = defineSentimento(dicio, result['text'], rePrefixo)
        date_time = processaData(result['created_at'])

        # Se identificou sentimento
        if sentimento_id != 0:
            # Se conseguiu inserir do db
            if insereTweet(c, result, sentimento_id, date_time) == 1:
                conn.commit()
                insereUsuario(c, result) # Adiciona usuario
                all_inseridos.append(result)
                count += 1
                conn.commit()

        else:
            f.write(result['text'].encode('utf-8')+'\n')

print "%s %d" % ('Foram inseridos:', count)
populaUsuarios(c, twitter, all_inseridos)
gravaUltimoTweet(c, all_results)

conn.commit()
f.close()
c.close()
