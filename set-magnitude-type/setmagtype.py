#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#                                                                          #
#    Copyright (C) 2015 by GFZ Potsdam                                     #
#                                                                          #
#    author: Joachim Saul                                                  #
#    email:  saul@gfz-potsdam.de                                           #
#                                                                          #
############################################################################

from __future__ import print_function
import sys, traceback, socket
import seiscomp3.DataModel
import sc3stuff.util
from sc3stuff.eventloader import EventLoaderApp


class PreferredMagnitudeTypeSetterApp(EventLoaderApp):

    def __init__(self, argc, argv):
        EventLoaderApp.__init__(self, argc, argv)
        self.setXmlEnabled(False)
        self.setMessagingEnabled(True)


    def createCommandLineDescription(self):
        if not EventLoaderApp.createCommandLineDescription(self):
            return False
        self.commandline().addGroup("Magnitude")
        self.commandline().addStringOption("Magnitude", "magnitude-type", "type of magnitude to set preferred")
        self.commandline().addStringOption("Magnitude", "dump-magnitude-types", "dump available magnitude types for this event")
        return True


    def validateParameters(self):
        if not EventLoaderApp.validateParameters(self):
            return False

        try:
            self._magType = self.commandline().optionString("magnitude-type")
        except:
            self._magType = None
        return True


#   def _getMagnitudeTypes(self):
#       return []


#   def _setPreferredMagnitudeType(self, magnitudeType):
#       # returns False if magnitude type cannot be set
#       # i.e. the magnitude is not available for this event
#       return True


    def sendJournal(self, action, params):
        j = seiscomp3.DataModel.JournalEntry()
        j.setObjectID(self._eventID)
        j.setAction(action)
        j.setParameters(params)
        j.setSender(self.name()+"@"+socket.gethostname())
        j.setCreated(seiscomp3.Core.Time.GMT())
        n = seiscomp3.DataModel.Notifier("Journaling", seiscomp3.DataModel.OP_ADD, j)
        nm = seiscomp3.DataModel.NotifierMessage()
        nm.attach(n)
        if not self.connection().send("EVENT", nm):
            return False
        return True


    def fixMw(self):
        return self.sendJournal("EvPrefMw", "true")

    def releaseMw(self):
        return sendJournal("EvPrefMw", "false")

    def fixMagnitudeType(self, magtype):
        return self.sendJournal("EvPrefMagType", "true")

    def releaseMagnitudeType(self):
        return sendJournal("EvPrefMagType", "")


    def run(self):
        if not EventLoaderApp.run(self):
            return False

        event, origin, pick, ampl, fm = sc3stuff.util.extractEventParameters(self._ep, self._eventID)
#       print(event, origin)

        if self._magType == "Mw":
            return self.fixMw()

        if self._magType[0].upper() == "M":
            return self.fixMagnitudeType(self._magType)

        raise ValueError, "Don't know what to do with magnitude %s" % self._magType


def main():
    app = PreferredMagnitudeTypeSetterApp(len(sys.argv), sys.argv)
    app()

if __name__ == "__main__":
    main()