# Copyright (c) 2017, Stephanie Wehner and Axel Dahlberg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by Stephanie Wehner, QuTech.
# 4. Neither the name of the QuTech organization nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging

from twisted.internet.defer import inlineCallbacks
from twisted.internet.protocol import Protocol, connectionDone

from cqc.cqcHeader import CQC_HDR_LENGTH, CQC_VERSION, CQCHeader

###############################################################################
#
# CQC Protocol
#
# Execute the CQC Protocol giving access to the SimulaQron backend via the
# universal interface.
#


class CQCProtocol(Protocol):
    # Dictionary storing the next unique qubit id for each used app_id
    _next_q_id = {}

    # Dictionary storing the next unique entanglement id for each used
    # (host_app_id,remote_node,remote_app_id)
    _next_ent_id = {}

    def __init__(self, factory):

        # CQC Factory, including our connection to the SimulaQron backend
        self.factory = factory

        # Default application ID, typically one connection per application but
        # we will deliberately NOT check for that since this is the task of
        # higher layers or an OS
        self.app_id = 0

        # Define the backend to use.
        self.messageHandler = factory.backend

        # Flag to determine whether we already received _all_ of the CQC header
        self.gotCQCHeader = False

        # Header for which we are currently processing a packet
        self.currHeader = None

        # Buffer received data (which may arrive in chunks)
        self.buf = None

        # Convenience
        self.name = self.factory.name

        logging.debug("CQC %s: Initialized Protocol", self.name)

    def connectionMade(self):
        pass

    def connectionLost(self, reason=connectionDone):
        pass

    def dataReceived(self, data):
        """
        Receive data. We will always wait to receive enough data for the
        header, and then the entire packet first before commencing processing.
        """
        # Read whatever we received into a buffer
        if self.buf:
            self.buf = self.buf + data
        else:
            self.buf = data

            # If we don't have the CQC header yet, try and read it in full.
        if not self.gotCQCHeader:
            if len(self.buf) < CQC_HDR_LENGTH:
                # Not enough data for CQC header, return and wait for the rest
                return

                # Got enough data for the CQC Header so read it in
            self.gotCQCHeader = True
            raw_header = self.buf[0:CQC_HDR_LENGTH]
            self.currHeader = CQCHeader(raw_header)

            # Remove the header from the buffer
            self.buf = self.buf[CQC_HDR_LENGTH: len(self.buf)]

            logging.debug("CQC %s: Read CQC Header: %s", self.name, self.currHeader.printable())

            # Check whether we already received all the data
        if len(self.buf) < self.currHeader.length:
            # Still waiting for data
            logging.debug(
                "CQC %s: Incomplete data. Waiting. Current length %s, " "required length %s",
                self.name,
                len(self.buf),
                self.currHeader.length,
            )
            return

            # We got the header and all the data for this packet. Start processing.
            # Update our app ID
        self.app_id = self.currHeader.app_id
        # Invoke the relevant message handler, processing the possibly
        # remaining data
        try:
            self._parseData(self.currHeader, self.buf[0: self.currHeader.length])
        except Exception as e:
            print(e)
            import traceback

            traceback.print_exc()

            # if self.currHeader.tp in self.messageHandlers:
            # 	self.messageHandlers[self.currHeader.tp](self.currHeader, )
            # else:
            # 	self._send_back_cqc(self.currHeader, CQC_ERR_UNSUPP)

            # Reset and await the next packet
        self.gotCQCHeader = False

        # Check if we received data already for the next packet, if so save it
        if self.currHeader.length < len(self.buf):
            self.buf = self.buf[self.currHeader.length: len(self.buf)]
            self.dataReceived(b"")
        else:
            self.buf = None

    @inlineCallbacks
    def _parseData(self, header, data):
        try:
            yield self.messageHandler.handle_cqc_message(header, data)
            messages = self.messageHandler.retrieve_return_messages()
        except Exception as e:
            raise e

        if messages:
            # self.factory._lock.acquire()
            for msg in messages:
                self.transport.write(msg)
                # self.factory._lock.release()

    def _send_back_cqc(self, header, msgType, length=0):
        """
        Return a simple CQC header with the specified type.

        header	 CQC header of the packet we respond to
        msgType  Message type to return
        length	 Length of additional message
        """
        hdr = CQCHeader()
        hdr.setVals(CQC_VERSION, msgType, header.app_id, length)

        msg = hdr.pack()
        self.transport.write(msg)
