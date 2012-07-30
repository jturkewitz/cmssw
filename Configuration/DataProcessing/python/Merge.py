#!/usr/bin/env python
"""
_Merge_

Module that generates standard merge job configurations for use in any
standard processing

"""


from FWCore.ParameterSet.Config import Process, EndPath
from FWCore.ParameterSet.Modules import OutputModule, Source, Service
import FWCore.ParameterSet.Types as CfgTypes


def mergeProcess(*inputFiles, **options):
    """
    _mergeProcess_

    Creates and returns a merge process that will merge the provided
    filenames

    supported options:

    - process_name : name of the procee, defaults to Merge
    - newDQMIO     : specifies if the new DQM format should be used to merge the files
    - output_file  : sets the output file name
    - output_lfn   : sets the output LFN

    """
    #  //
    # // process supported options
    #//
    processName = options.get("process_name", "Merge")
    outputFilename = options.get("output_file", "Merged.root")
    outputLFN = options.get("output_lfn", None)
    dropDQM = options.get("drop_dqm", False)
    newDQMIO = options.get("newDQMIO", False)
    
    #  //
    # // build process
    #//
    process = Process(processName)

    #  //
    # // input source
    #//
    if newDQMIO:
        process.source = Source("DQMRootSource")
        process.Merged = OutputModule("DQMRootOutputModule")
        process.add_(Service("DQMStore"))
    else:
        process.source = Source("PoolSource")
        process.Merged = OutputModule("PoolOutputModule")
        if dropDQM:
            process.source.inputCommands = CfgTypes.untracked.vstring('keep *','drop *_EDMtoMEConverter_*_*')
    process.source.fileNames = CfgTypes.untracked(CfgTypes.vstring())
    for entry in inputFiles:
        process.source.fileNames.append(str(entry))
 
    #  //
    # // output module
    #//
    process.Merged.fileName = CfgTypes.untracked(CfgTypes.string(
        outputFilename))

    if outputLFN != None:
        process.Merged.logicalFileName = CfgTypes.untracked(CfgTypes.string(
            outputLFN))


    process.outputPath = EndPath(process.Merged)
    return process
