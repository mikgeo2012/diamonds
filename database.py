# from tinydb import TinyDB, Query, where
# from singleton import singleton
# import utils as ut
# import web_scraper as webScr
# from operator import itemgetter

# @singleton
# class DataBase:

#     def __init__(self):
#         self.db = TinyDB('data.json')

#     def store(self, diamond):
#         print("Storing data")

#         di = self.db.search(where('uuid') == diamond['uuid'])

#         if not di:
#             self.db.insert(diamond)
#         elif len(di) == 1:
#             self.db.update(diamond, where('uuid') == di['uuid'])

#         print diamond['url']


#     def returnAll(self):
#         return self.db.all()

#     def clean(self):
#         self.db.purge()
#         self.db.all()

#     def returnGood(self):
#         result = []
#         temp = self.db.all()

#         for i in temp:
#             # if float(i['cut_score']) >= 95.0 and float(i['hca_score']) <= 2.0 and float(i['di/crt'][0]) >= float(i['di/crt'][1]):
#             #     result.append(i)

#             if float(i['cut_score']) >= 95.0 and float(i['hca_score']) <= 2.0:
#                 result.append(i)

#         return result

#     def returnUrls(self):
#         result = []
#         temp = self.db.all()

#         for i in temp:
#             result.append(i['url'])

#         return result

#     def refreshDB(self):
#         temp = self.db.all()

#         for i in temp:
#             isAvailable = webScr.parseForAvailability(i['url'])
#             if not isAvailable:
#                 self.db.remoave(doc_ids=i.doc_id)
#                 print "Removed {0}".format(i['gia_num'])


#     def returnSorted(self, key, descending = True):
#         temp = self.returnAll()
#         if key == 'di/crt':
#             return sorted(temp, key=lambda k: float(k['di/crt'][1]) - float(k['di/crt'][0]))

#         return sorted(temp, key=itemgetter(key), reverse = descending)


