import nltk
import pickle
import sqlite3

def connectDB():
    connect = sqlite3.connect('beta.sqlite')
    cur = connect.cursor()
    return connect, cur

connect, cur = connectDB()

def tobepop(cur):        #figure out the extra rows in sents that have to be populated in words
    cur.execute('select max(id) from words;')
    st = cur.fetchone()
    if not st or st==None:
        return 0,0
    cur.execute('select max(id) from sents;')
    end = cur.fetchone()
    return st[0]+1, end[0]

def Noun(word, cur, m):
    cur.execute('select id from words where noun1 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set noun1=? where id=?;',  (word, d[0]))
        return
    cur.execute('select id from words where noun2 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set noun2=? where id=?;',  (word, d[0]))
        return
    cur.execute('select id from words where noun3 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set noun3=? where id=?;',  (word, d[0]))
        return
    cur.execute('select id from words where noun4 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set noun4=? where id=?;',  (word, d[0]))
        return

def Pronoun(word, cur, m):
    cur.execute('select id from words where noun1 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set noun1=? where id=?;',  (word, d[0]))
        return
    cur.execute('select id from words where noun2 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set noun2=? where id=?;',  (word, d[0]))
        return
    cur.execute('select id from words where noun3 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set noun3=? where id=?;',  (word, d[0]))
        return
    cur.execute('select id from words where noun4 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set noun4=? where id=?;',  (word, d[0]))
        return


def Adjective(word,cur, m):
    cur.execute('select id from words where adj1 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set adj1=? where id=?;',  (word, d[0]))
        return
    cur.execute('select id from words where adj2 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set adj2=? where id=?;',  (word, d[0]))
        return
    cur.execute('select id from words where adj3 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set adj3=? where id=?;',  (word, d[0]))
        return


def Modal(word,cur, m):
    cur.execute('select id from words where modal IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set modal=? where id=?;',  (word, d[0]))
        return


def Verb(word,cur, m):
    cur.execute('select id from words where verb1 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set verb1=? where id=?;',  (word, d[0]))
        return

    cur.execute('select id from words where verb2 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set verb2=? where id=?;',  (word, d[0]))
        return
    cur.execute('select id from words where verb3 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set verb3=? where id=?;',  (word, d[0]))
        return



def wh(word,cur, m):
    cur.execute('select id from words where wh IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set wh=? where id=?',  (word, d[0]))
        return


def Adverb(word,cur, m):
    cur.execute('select id from words where adv1 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set adv1=? where id=?;',  (word, d[0]))
        return

    cur.execute('select id from words where adv2 IS NULL and new = 1;')
    d = cur.fetchone()
    if d:
        cur.execute('update words set adv2=? where id=?;',  (word, d[0]))
        return

weights = {}      #the dictionary of weights assigned. This is updated for every new input.

ratings = {'N':8, 'V': 10, 'P':6, 'J': 0.8, 'R':0.4, 'W':6, 'M': 6}  #relative ratings of the parts of speech.

def finddenom(worddict, cur):                #function to find the total weight of the current sentence.
    total = 0
    for word in worddict:
        if word in wordval:
            weights[word] = 1/wordval[word]      #weight = 1/(its occurence in the corpora)
        else:
            weights[word]=0.1
    for i in worddict:
        pos = worddict[i]
        pos = pos[0]
        if pos in ratings:
            weights[i] = weights[i]*ratings[pos]   #weights * rating of the POS.
            total = total+ weights[i]
    print('in finddenom')
    cur.execute('update words set denom=? where new=?;', (total, 1))
    return total, weights

def stop_remove(sent):       
    from nltk.corpus import stopwords
    stop=stopwords.words('english')
    final={}
    for i in sent:
        if i in ['.', '?', ',','!']:
            continue
        if i not in stop:
            final[i]=sent[i]    
    return final
    
    
cats = { 'N' : Noun,
         'J' : Adjective,
         'M' : Modal,
         'V' : Verb,
         'W' : wh,
         'R' : Adverb,
         'P' : Pronoun,
         }



st, end = tobepop(cur)
if st==0:
    exit()
for i in range(st, end+1):
    cur.execute('select Input from sents where id>? and id=?;', (0, i))
    inp = cur.fetchone()[0]
    wordlist = nltk.word_tokenize(inp)
    worddict = nltk.pos_tag(wordlist)       #pos tagged dictionary of the words of the sentence.                #duplicates removed.
    worddict = dict(worddict)
    wordlist = list(worddict.keys())   #duplicates have been removed now, both in wordlist and worddict.
    newdict = stop_remove(worddict)
    index = 0
    q = 'insert into words(id) values(' + str(i) + ')'
    print(i)
    cur.execute(q)
    cur.execute('update words set new=? where id=?;', (1, i))
    cur.execute('select id from words where new=1;')
    m = cur.fetchone()
    m = m[0]
    while(index<len(wordlist)):
          #cur.execute('select id from words where new = 1;')
          #Id = cur.fetchone()
          #Id = Id[0]
          word = wordlist[index]
          char = worddict[word]
          char = char[0]            #current word's pos tag.
          if char[0] not in cats.keys():
              index = index+1
              continue
          cats[char](word, cur, m)     #function call corresponding to the pos tag to insert the word in the right column in a new record in the database,
          index = index+1
    connect.commit()
    #cur.execute('select * from words where id = 2')
    output = open('density.txt', 'rb')      #file containing the dictionary of frequency of words in the corpora is opened.
    wordval = pickle.load(output)
    inpval, weights = finddenom(worddict, cur)      #find the weight of the current sentence, for future use.
    cur.execute('update words set sentkey=? where id=?;', (i, i))
    cur.execute('update words set new=? where id=?;', (0, i))
    connect.commit()
connect.close()
