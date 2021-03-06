#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Super Class of the managed datatype
"""

import os
import tempfile
import collections
import util
import logging
import abc
from abc import ABCMeta
from TrackDb import TrackDb
from datatypes.validators.DataValidation import DataValidation


class Datatype(object):
    __metaclass__ = ABCMeta

    twoBitFile = None
    chromSizesFile = None
    input_fasta_file = None
    extra_files_path = None
    tool_directory = None

    mySpecieFolderPath = None
    myTrackFolderPath = None
 

    def __init__(self):
        not_init_message = "The {0} is not initialized." \
                           "Did you use pre_init static method first?"
        if Datatype.input_fasta_file is None:
            raise TypeError(not_init_message.format('reference genome'))
        if Datatype.extra_files_path is None:
            raise TypeError(not_init_message.format('track Hub path'))
        if Datatype.tool_directory is None:
            raise TypeError(not_init_message.format('tool directory'))
        self.inputFile = None
        self.trackType = None
        self.dataType = None
        self.track = None
        self.trackSettings = dict()
        self.extraSettings = collections.OrderedDict()

    @staticmethod
    def pre_init(reference_genome, two_bit_path, chrom_sizes_file,
                 extra_files_path, tool_directory, specie_folder, tracks_folder):
        Datatype.extra_files_path = extra_files_path
        Datatype.tool_directory = tool_directory

        # TODO: All this should be in TrackHub and not in Datatype
        Datatype.mySpecieFolderPath = specie_folder
        Datatype.myTrackFolderPath = tracks_folder

        Datatype.input_fasta_file = reference_genome

        # 2bit file creation from input fasta
        Datatype.twoBitFile = two_bit_path
        Datatype.chromSizesFile = chrom_sizes_file
    
    def generateCustomTrack(self):
        self.validateData()
        self.initSettings()
        #Create the track file
        self.createTrack()
        # Create the TrackDb Object
        self.createTrackDb()
        logging.debug("- %s %s created", self.dataType, self.trackName)  

    
    @abc.abstractmethod 
    def validateData(self):
        """validate the input data with DataValidation"""
    
    def initSettings(self):
        #Initialize required fields: trackName, longLabel, shortLable
        self.trackName = self.trackSettings["name"]
        if self.trackSettings["long_label"]:
            self.longLabel = self.trackSettings["long_label"]
        else:
            self.longLabel = self.trackName
        if not "short_label" in self.trackSettings:
            self.shortLabel = ""
        else:
            self.shortLabel = self.trackSettings["short_label"]
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        

    @abc.abstractmethod
    def createTrack(self):
        """Create the final track file"""

    def createTrackDb(self):
        self.track = TrackDb(self.trackName, self.longLabel, self.shortLabel, self.trackDataURL, self.trackType, self.extraSettings)

