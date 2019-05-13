import pickle
import pandas as pd
import dash_html_components as html
import requests

loadModel = pickle.load(open('rfc_pokemon.sav', 'rb'))
encoderType1 = pickle.load(open('le_type1.sav', 'rb'))
encoderType2 = pickle.load(open('le_type2.sav', 'rb'))

def callbackpredict(n_clicks,name,type1,type2,gen,total,hp,attack,defense,spatk,spdef,speed):
    if(name!='' and type1 !='' and type2!='' and gen!='' and total!='' and hp!='' and attack!='' and defense!='' and spatk!='' and spdef!='' and speed!=''):
        etype1 = encoderType1.transform([type1])
        etype2 = encoderType2.transform([type2])
        dataPredict = pd.DataFrame([[etype1[0],etype2[0],gen,total,hp,attack,defense,spatk,spdef,speed]])
        predictProb = loadModel.predict_proba(pd.DataFrame(dataPredict))
        predict = ''
        predictSave = 0
        for prob in predictProb[:,1]:
            if(prob > 0.15):
                predict = 'Legendary'
                predictSave = 1
            else:
                predict = 'Normal'
        perc = (predictProb[0][1] * 100)

        data = {
            'name' : name,
            'type1' : type1,
            'type2' : type2,
            'generation' : int(gen),
            'total' : int(total),
            'hp' : int(hp),
            'attack' : int(attack),
            'defense' : int(defense),
            'spatk' : int(spatk),
            'spdef' : int(spdef),
            'speed' : int(speed),
            'legendary' : predictSave,
            'legendaryProba' : predictProb[0,1],
            'createdby' : "Glen"
        }
        res = requests.post('http://api-pokemon-baron.herokuapp.com/saveprediction', data = data)
        print(res.content)

        return [
            html.H3('Probability your Pokemon is Legendary : ' + str(perc) + '%,'),
            html.H3('So we predict ' + str(name) + ' is a ' + str(predict) + ' Pokemon')
        ]
    else:
        return html.H3('Please fill all inputs in the form above to Predict your Pokemon')