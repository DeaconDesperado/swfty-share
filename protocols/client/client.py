from twisted.web import proxy
from twisted.internet import reactor,protocol,defer,stdio
from twisted.python import log
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.protocols import basic
import sys
import json
from json_encoder import Encoder
from bson.objectid import ObjectId
import os

log.startLogging(sys.stdout)

TEST_DATA = '/home/mark/projects/swfty/test.csv'

class ClientProtocol(protocol.Protocol):

    def connectionMade(self):
        self.json_string = json.dumps({
            'uid':ObjectId(),
            'lat':43.78,
            'lon':-72.5831
        },cls=Encoder)
        self.fileObject = open(TEST_DATA)
        self.totalSize = os.stat(TEST_DATA).st_size
        self.uploaded = 0

    def start(self):
        self.transport.write('OPN|'+self.json_string)

    def sendFile(self):
        lineData = self.fileObject.readline()
        if lineData != '':
            self.transport.write('UPD|')
            self.transport.write(lineData)
            self.uploaded+=len(lineData)
        else:
            self.transport.write('EOF|done')

    def dataReceived(self,data):
        if data in ['ELLO','RECVD']:
            self.sendFile()
            print '%s percent of the file has been uploaded' % (float(self.uploaded)/float(self.totalSize))



class ClientFactory(protocol.ClientFactory):
    protocol = ClientProtocol
    def buildProtocol(self,addr):
        return ClientProtocol()


class SendClient(basic.LineReceiver):
    delimiter = "\n"
    prompt_string = '>>>'

    def prompt(self):
        self.transport.write(self.prompt_string)

    def connectionMade(self):
        self.sendLine('Test server')
        self.factory = ClientFactory()
        self.connector = reactor.connectTCP('localhost',5000,self.factory)
        print self.connector
        self.prompt()

    def lineReceived(self,line):
        if not line:
            self.prompt()
            return
        self.issueCommand(line)

    def issueCommand(self,command):
        func = getattr(self.connector.transport,command)
        func()

if __name__ == '__main__':
    stdio.StandardIO(SendClient())
    reactor.run()
