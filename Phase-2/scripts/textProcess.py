import json
import requests
import spacy
from spacy.matcher import Matcher
import spacy_dbpedia_spotlight

pattern=[{"LOWER": "communication"}]
blackListWords=["COMP","COEN","Google","Moodle",'midterm exam',"Midterm","Concordia","Concordia University"]


class TextProcessor:
    def __init__(self):
        self.nlp=spacy.load('en_core_web_md')
        self.nlp.add_pipe('entityfishing')
        #self.nlp.add_pipe('dbpedia_spotlight',config={'dbpedia_rest_endpoint': 'http://localhost:2222/rest'},last=True)

        self.matcher=Matcher(self.nlp.vocab)
        self.matcher.add('ent_identifier',[pattern])


    def processText(self, text):
        self.doc=self.nlp(text)
        
        # for ent in self.doc.ents:
        #     print(ent.text,ent.label_)
        #wikidataLinks=self.getFishingResult()
        #print('fish',wikidataLinks)
        #dbspotlinks=self.getDbResult()
        #print(self.doc.ents)
        # for i in dbspotlinks:
        #     matches = self.matcher(i)
        #     for match_id, start, end in matches:
        #         string_id = self.nlp.vocab.strings[match_id]  # String representation
        #         span = self.doc[start:end]  # Matched span
        #         print("Match found:", string_id, span.text, "at positions:", start, end)
           #DBPEDIA_ENT            
        wikiResult=self.getFishingResult()
        dbresult=self.getDbResult()
       
        
        return wikiResult,dbresult



    def getFishingResult(self):
        dbresult={}
        dbscore={}
        wikiResult={}
        wikiScore={}
        for ent in self.doc.ents:
            #print(ent.label_,ent._.dbpedia_raw_result['@similarityScore'])
            if ent.text in blackListWords:
                continue
            # if ent.kb_id_ is not None:
              
            #     if float(ent._.dbpedia_raw_result['@similarityScore'])>0.89 and float(ent._.dbpedia_raw_result["@percentageOfSecondRank"])<0.2:
            #         if ent not in dbresult:
            #             dbresult[ent.text]=ent.kb_id_
            #             dbscore[ent.text]=float(ent._.dbpedia_raw_result['@similarityScore'])

            #         elif dbscore[ent.text]<float(ent._.dbpedia_raw_result['@similarityScore']):
            #             dbresult[ent.text]=ent.kb_id_
            #             dbscore[ent.text]=float(ent._.dbpedia_raw_result['@similarityScore'])
            #         else:
            #             continue

            if ent._.url_wikidata is not None:
                if ent.text not in wikiResult and ent._.nerd_score>0.66:
                    wikiResult[ent.text]=ent._.url_wikidata
                    wikiScore[ent.text]=ent._.nerd_score
                elif ent.text in wikiResult and ent._.nerd_score>wikiScore[ent.text]:
                    wikiResult[ent.text]=ent._.url_wikidata
                    wikiScore[ent.text]=ent._.nerd_score
                else:
                    continue
        return wikiResult
    
    def getDbResult(self):
        #print("db spotlight")
        result={}
        score={}

        for sent in self.doc.sents:
            if len(sent.text.strip().replace("\n", "").replace("\t", "").replace(" ", ""))==0:
                continue
            url="http://localhost:2222/rest/annotate?text="+sent.text
            req=requests.get(url=url,headers={"accept":"application/json"})
           
            if req.status_code!=200:
                print(sent.text ,req.status_code,req.text)
                continue
            res=req.json()
            #print('op',res)
            if "Resources" not in res:
                continue
            for i in res["Resources"]:
                
                if float(i["@similarityScore"])>0.89 and float(i["@percentageOfSecondRank"])<0.2:
                    if i["@surfaceForm"] not in result:
                        result[i["@surfaceForm"]]=i["@URI"]
                        score[i["@surfaceForm"]]=float(i["@similarityScore"])

                    elif score[i["@surfaceForm"]]<float(i["@similarityScore"]):
                        result[i["@surfaceForm"]]=i["@URI"]
                        score[i["@surfaceForm"]]=float(i["@similarityScore"])
                    else:
                        continue
                else:
                    continue
        return result
            

                        


