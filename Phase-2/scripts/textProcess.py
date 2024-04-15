import json
import requests
import spacy
import spacy.matcher
import spacy_dbpedia_spotlight
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy.language import Language
from spacy.tokens import Doc


# nlp=spacy.load('en_core_web_md')
pattern=[{"LOWER": "communication"}]
macthedWords=[]
blackListEnts=[]
blackListWords=['moodle','movie','lab',"introduction","comp","coen","midterm","concordia","university","google","exam","sn","eof"]
pattern =[ 
 [{"POS": "PROPN"}, {"POS": "PROPN", "OP": "+"}],
 [{"POS": "NOUN"}, {"POS": "NOUN", "OP": "+"}],
[
    
    {"POS": "ADJ", "OP": "?"},
    {"POS": "PROPN"},            # Proper noun (NNP)

],
[
    
    {"POS": "ADJ", "OP": "?"},
    {"POS": "PROPN"},            # Proper noun (NNP)
    {"POS": "NOUN", "OP": "?"},  # Optional noun (NN)
    {"POS": "PROPN", "OP": "?"}, # Optional proper noun (NNP)
    {"POS": {"IN": ["IN"]}, "OP": "?"}, # Optional preposition (IN)
    {"POS": "PROPN", "OP": "?"}  # Optional proper noun (NNP)
],
[{"IS_TITLE": True}],
[
    {"POS": "PROPN"},   # Proper noun (NNP)
    {"TEXT": "-"},      # Hyphen
    {"POS": {"IN": ["PROPN", "NOUN", "ADJ"]}}  # Proper noun (NNP), noun (NN), or adjective (JJ)
]

]
@Language.component('macther')
def matcher(doc):
    global macthedWords
    matcher = spacy.matcher.Matcher(doc.vocab)
    matcher.add("COMBINATIONS", pattern)
    matches= matcher(doc)

    # # for i in doc:
    # #     print("text",i.text,"tag",i.tag_ ,"LEN",len(i.text))

    # # Add the pattern to the matcher
    # matcher.add("COMBINATIONS", pattern)

    # # Apply the matcher to the document
    # matches = matcher(doc)

    # # Process the matches
    # # for match_id, start, end in matches:

    # #     # Create a Span for the matched tokens
    # #     span = Span(doc, start, end, label="COMBINATIONS")
    # #     print("txt",span)
    # #     if span not in doc.ents:
    # #     # Add the Span to the document's entities
    # #         doc.ents = list(doc.ents) + [span]
    # entity_indices = []
    # for match_id, start, end in matches:
    #     # Add the indices of tokens in the matched span to the list
    #     entity_indices.extend(range(start, end))

    # # Remove duplicate indices
    # entity_indices = list(set(entity_indices))
    entities = []
    for match_id, start, end in matches:
        string_id = doc.vocab.strings[match_id]  # String representation
        span = doc[start:end]  # Matched span
        print("Match found:", string_id, span.text, "at positions:", start, end)
        entities.append(span.text)
    # Create a new list to store the entities
    

    # Process the entity indices
    # for i in entity_indices:
    #     # Create a Span for each token
    #     span = doc[i:i+1]
        
    #     # Append the Span to the list of entities
    #     entities.append(span)

    # Set the entities for the document
    #print(list(entities))
    #doc.ents = []
    text=[]
    for i in entities:
        text.append(i)
    macthedWords=text
    #print("doc",doc.user_data)
    #doc.vocab.add_flag(lambda x: x in text)
    return doc
    
    #return Doc(vocab=doc.vocab,words=text)
@Language.component('remove_tokens')
def remove_tokens(doc):
    filtered_tokens = [token.text for token in doc if token.text.lower() not in blackListWords]

    # Return the modified document
    return Doc(doc.vocab, words=filtered_tokens)

@Language.component('remove_ner')
def remove_ner(doc):
    global macthedWords
    global blackListEnts
    #print(" match",macthedWords)
    # for ent in doc.ents:
    #     print(ent.text,ent.label_)
    for i in doc.ents:
        if i.label_ in ["LOC","GPE","MONEY","PERSON","CARDINAL","ORDINAL","TIME"]:
            
            blackListEnts.append(i.text.lower())
    new_ents = [ent for ent in doc.ents if ent.label_ not in ["LOC","GPE","MONEY","PERSON"] ]
    doc.ents = new_ents
    
    #print(doc.ents)
    #words=[]
    # for i in new_ents:
    #     words.append(i.text)
    return doc






class TextProcessor:
    def __init__(self):
        self.nlp=spacy.load('en_core_web_md')
        spacy.tokens.Doc.set_extension("user_data", default=None, force=True)
        print("Pipeline components:")
        # print(self.nlp.pipe_names)
        self.nlp.remove_pipe("ner")
        self.nlp.add_pipe("ner", source=spacy.load("en_core_web_md"))

        # add entity ruler
        self.nlp.add_pipe('macther',name="ent_matcher",before="ner")
        #nlp.add_pipe("entity_ruler", before="ner")
        self.nlp.add_pipe("remove_tokens",name="remove_tokens",after="ent_matcher")
        self.nlp.add_pipe("remove_ner",name="remove_ner",after="ner")
        #self.nlp.add_pipe('macther',name="ent_matcher",after="ner")
        self.nlp.add_pipe('entityfishing')
        self.nlp.add_pipe('dbpedia_spotlight',config={'dbpedia_rest_endpoint': 'http://localhost:2222/rest','raise_http_errors': False},last=True)
        print(self.nlp.pipe_names)
        

    

    def processText(self, text):
        self.doc=self.nlp(text)
        #print(self.doc.ents)
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
        wikiResult, dbresult=self.getFishingResult()
        #dbresult=self.getDbResult()
        #print(dbresult)
        dbresult=self.processDBresult(dbresult)
        wikiResult=self.processDBresult(wikiResult)
        return wikiResult,dbresult


    def processDBresult(self,listDb):
        
        global macthedWords
        global blackListEnts
        # for i in self.doc.ents:
        #     print(i,i.label_)
        # Filter out entities from DBpedia Spotlight that match the Matcher
        filtered_entities = [entity for entity in listDb if entity in macthedWords and entity.lower() not in blackListEnts ]
        res={}
        for i in filtered_entities:
            if i in listDb:
                res[i]=listDb[i]
        #print(macthedWords)
        return res

    def getFishingResult(self):
        dbresult={}
        dbscore={}
        wikiResult={}
        wikiScore={}
        for ent in self.doc.ents:
            #print(ent.label_,ent._.dbpedia_raw_result['@similarityScore'])
            if ent.text in blackListWords:
                continue
            if ent.kb_id_ is not None and ent._.dbpedia_raw_result is not None:
              
                if float(ent._.dbpedia_raw_result['@similarityScore'])>0.89 and float(ent._.dbpedia_raw_result["@percentageOfSecondRank"])<0.2:
                    if ent not in dbresult:
                        dbresult[ent.text]=ent.kb_id_
                        dbscore[ent.text]=float(ent._.dbpedia_raw_result['@similarityScore'])

                    elif dbscore[ent.text]<float(ent._.dbpedia_raw_result['@similarityScore']):
                        dbresult[ent.text]=ent.kb_id_
                        dbscore[ent.text]=float(ent._.dbpedia_raw_result['@similarityScore'])
                    else:
                        continue

            if ent._.url_wikidata is not None:
                if ent.text not in wikiResult and ent._.nerd_score>0.66:
                    wikiResult[ent.text]=ent._.url_wikidata
                    wikiScore[ent.text]=ent._.nerd_score
                elif ent.text in wikiResult and ent._.nerd_score>wikiScore[ent.text]:
                    wikiResult[ent.text]=ent._.url_wikidata
                    wikiScore[ent.text]=ent._.nerd_score
                else:
                    continue
        return [wikiResult,dbresult]
    
    # def getDbResult(self):
    #     #print("db spotlight")
    #     result={}
    #     score={}

    #     for sent in self.doc.sents:
    #         if len(sent.text.strip().replace("\n", "").replace("\t", "").replace(" ", ""))==0:
    #             continue
    #         url="http://localhost:2222/rest/annotate?text="+sent.text
    #         req=requests.get(url=url,headers={"accept":"application/json"})
           
    #         if req.status_code!=200:
    #             print("sent",sent.text ,"code ",req.status_code,req.text)
    #             continue
    #         res=req.json()
    #         #print('op',res)
    #         if "Resources" not in res:
    #             continue
    #         for i in res["Resources"]:
                
    #             if float(i["@similarityScore"])>0.89 and float(i["@percentageOfSecondRank"])<0.2:
    #                 if i["@surfaceForm"] not in result:
    #                     result[i["@surfaceForm"]]=i["@URI"]
    #                     score[i["@surfaceForm"]]=float(i["@similarityScore"])

    #                 elif score[i["@surfaceForm"]]<float(i["@similarityScore"]):
    #                     result[i["@surfaceForm"]]=i["@URI"]
    #                     score[i["@surfaceForm"]]=float(i["@similarityScore"])
    #                 else:
    #                     continue
    #             else:
    #                 continue
    #     return result
            

                        


