"""This module defines the twisted protocol that will incrementally accept files from the client device"""

from twisted.web import proxy
from twisted.internet import reactor,protocol
from twisted.python import log
import sys

log.startLogging(sys.stdout)

class TransferProtocol(protocol.Protocol):

    ran = 0

    def connectionLost(self,reason):
        print reason

    def connectionMade(self):
        self.fileObject = open('output','w')

    def dataReceived(self,data):
        methods = {'OPN':'open','UPD':'upload','EOF':'endfile'}
        if data[0:3] in methods.keys():
            func = getattr(self,methods[data[0:3]])
            func(data[4:])

    def open(self,data):
        print 'OPEN %s' % data
        self.transport.write('ELLO')

    def endfile(self,data):
        print 'END %s' % data
        self.transport.loseConnection()

    def upload(self,data):
        self.ran+=1
        self.fileObject.write(data)
        self.transport.write('RECVD')


class myProtocolFactory(protocol.Factory):
    protocol = TransferProtocol

    def doStart(self):
        pass

    def startedConnecting(self, connectorInstance):
        print connectorInstance

    def buildProtocol(self, address):
        print address
        return self.protocol()

    def clientConnectionLost(self, connection, reason):
        print reason
        print connection

    def clientConnectionFailed(self, connection, reason):
        print connection
        print reason

    def doStop(self):
        pass

if __name__ == '__main__':
    reactor.listenTCP(5000, myProtocolFactory())
    reactor.run()
