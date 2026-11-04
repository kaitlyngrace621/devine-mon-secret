from http.server import BaseHTTPRequestHandler
import os, json, hmac
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

PROMPT = 'Tu es le moteur d\'un jeu de devinettes français pour enfants de 6 à 12 ans.\nLe mot secret est fourni séparément par le programme. Ne le révèle jamais.\nInterprète TOUTES les formulations de questions françaises courantes, même familières, elliptiques, imparfaites, avec ou sans point d\'interrogation, et les reformulations.\nL\'élève peut demander « un crayon ? », « tu es un crayon ? », « est-ce que c\'est un crayon ? » ou un synonyme. Dans ce cas kind="guess". yes=true si le nom proposé désigne réellement le même objet ou animal que le mot secret; sinon false. Fais attention à distinguer une catégorie générale (« tu es un meuble ? ») d\'une vraie proposition d\'identité (« tu es une table ? »).\nSi l\'élève pose une question sur une propriété (lieu, fréquence dans une maison, matière, taille, couleur, utilité, animal, meuble, réalité ou personnage imaginaire, nourriture, habitat, action, etc.), kind="question" et yes=true ou false selon les faits ordinaires et une interprétation raisonnable. Une question peut être indirecte (« c\'est quelque chose dans une salle de bain ? »). Si « parfois » ou « souvent » est sous-entendu, réponds en te fondant sur ce qui est habituel. Ne considère pas qu\'un objet soit dans toutes les pièces d\'une maison.\nSi la question est réellement incompréhensible, kind="unclear" et yes=false. Ne dis pas que tu ne comprends pas uniquement parce que la phrase est originale.\nTu n\'es pas en train de converser librement : ne donne jamais de nom, d\'indice gratuit ou d\'explication avant la fin du jeu. Réponds UNIQUEMENT sous forme de JSON valide avec ces clés : kind (guess/question/unclear), yes (booléen), topic (un des mots : salle_de_bain,meuble,animal,maison,frequent_maison,ecole,cuisine,salon,chambre,existence,vivant,dehors,eau,volant,mangeable,material,ecriture,bruit,petit,grand,electrique,imaginaire,color,start). Choisis le sujet le plus proche ou start.'

class handler(BaseHTTPRequestHandler):
    def send_json(self, status, item):
        raw=json.dumps(item,ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Length',str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        key=os.environ.get('OPENAI_API_KEY','')
        gate=os.environ.get('GAME_ACCESS_CODE','')
        if not key or not gate:
            return self.send_json(503, {'error':'Mode IA non configuré'})
        provided=self.headers.get('X-Game-Code','')
        if not hmac.compare_digest(provided,gate):
            return self.send_json(401, {'error':'Code d’accès incorrect'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if length<1 or length>15000:
                return self.send_json(413,{'error':'Message trop long'})
            data=json.loads(self.rfile.read(length))
            secret=data['secret']; question=data['question']; theme=data.get('theme','mix')
            if not isinstance(secret,str) or not isinstance(question,str) or len(secret)>120 or len(question)>300:
                return self.send_json(400,{'error':'Message invalide'})
            history=data.get('history',[])
            if not isinstance(history,list): history=[]
            history=[item for item in history[-12:] if isinstance(item,dict)]
            request_body={
              'model': os.environ.get('OPENAI_MODEL','gpt-4.1-mini'),
              'temperature':0,
              'response_format':{'type':'json_object'},
              'messages':[{'role':'system','content':PROMPT},
                  {'role':'user','content':json.dumps({'mot_secret':secret,'theme':theme,'question_de_l_eleve':question,'questions_precedentes':history},ensure_ascii=False)}]
            }
            request=Request('https://api.openai.com/v1/chat/completions',data=json.dumps(request_body).encode('utf-8'),
                headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
            with urlopen(request,timeout=25) as response:
                raw=json.loads(response.read(100000))
            a=json.loads(raw['choices'][0]['message']['content'])
            kind=a.get('kind'); yes=a.get('yes'); topic=a.get('topic','start')
            if kind not in ('guess','question','unclear') or not isinstance(yes,bool):
                raise ValueError('Réponse du modèle invalide')
            if not isinstance(topic,str) or len(topic)>40: topic='start'
            return self.send_json(200,{'kind':kind,'yes':yes,'topic':topic})
        except (HTTPError,URLError,TimeoutError):
            return self.send_json(502,{'error':'Connexion IA temporairement indisponible'})
        except Exception:
            return self.send_json(502,{'error':'Réponse IA indisponible'})
