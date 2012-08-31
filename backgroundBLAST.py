#!/usr/bin/python
# File: backgroundBLAST.py
# Desc: Runs a (daily) BLAST search and looks for new homologs

import sys, time, urllib, urllib2, pynotify, logging, optparse

#Basic URLs we need to submitt REST requests
base_url = 'http://www.ebi.ac.uk/Tools/services/rest/ncbiblast/'
run_url = base_url + 'run/'
status_url = base_url + 'status/'
result_url = base_url + 'result/'

url_data = {'title' : 'backgroundBLAST.py Request',
	'dropoff' : 0,
	'matrix' : 'BLOSUM62',
	'database' : 'uniprotkb',
	'program' : 'blastp',
	'exp' : 1.0,
	'scores' : 1000,
	'alignments' : 1000,
	'email' : 'gmshoffner@gmail.com',
	'sequence' : '',
	'stype' : 'protein'}

def setupCommandLineParser():
	"""Runs optparse to parse command line input"""
	Usage = "python backgroundBLAST.py [OPTIONS] sequence_file.fasta"
	Parser = optparse.OptionParser(Usage)
	#Add some options later...
	(CmdLineOps, Args) = Parser.parse_args()
	if len(Args) == 0:
		logging.error(Usage)
		sys.exit()
	return (CmdLineOps, Args)


def readSeqFile(file_name):
	#Could add some sequence validation here
	with open(file_name) as sequence_file:
		sequence = sequence_file.read()
	return sequence

def readIdentifierFile(file_name):
	with open(file_name) as identifier_file:
		identifiers = identifier_file.read().split('\n')
	return identifiers


def runRequest(url_data):
	url = urllib.urlencode(url_data)
	Request = urllib2.urlopen(run_url, url)
	return Request.read()


def statusRequest(jobID):
	url = status_url + jobID
	Status = urllib2.urlopen(url)
	return Status.read()


def resultRequest(jobID):
	url = result_url + jobID + '/ids'
	Result = urllib2.urlopen(url)
	return Result.read()


def main():
	(CmdLineOps, Args) = setupCommandLineParser()
	seq_file_name = Args[0]
	id_file_name = Args[1]
	sequence_ids = readIdentifierFile(id_file_name)
	url_data['sequence'] = readSeqFile(seq_file_name)
	while True:
		StartNotify = pynotify.Notification("Running today's BLAST search")
		StartNotify.show()
		jobID = runRequest(url_data)
		time.sleep(30)
		job_status = statusRequest(jobID)
		while job_status == 'RUNNING':
			time.sleep(30)
			job_status = statusRequest(jobID)
		Result = resultRequest(jobID)
		result_ids = Result.split('\n')
		new_ids = [seq_id for seq_id in result_ids if seq_id not in sequence_ids]
		if new_ids:
			print new_ids
			Notify = pynotify.Notification("Found new sequence homologs!")
			Notify.show()
			sys.exit(0)
		time.sleep(60)



if __name__ == '__main__':
	main()
