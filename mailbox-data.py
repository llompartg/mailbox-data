import re
import mailbox
import csv
import argparse

class MailBoxDataProcessor:
	def __init__(self, path):
		self.results = {}
		self.path = path

	def __increase_count(self, sender):
		if sender in results:
			results[sender]+=1
		else:
			results[sender] = 1

	def run(self):
		for message in mailbox.mbox(self.path):
			sender = message["from"]
			if "<" in sender:
				# Emails might come between <>
				mail = re.search("<(.*?)>", sender).group(1)
				self.__increase_count(mail)
			else:
				self.__increase_count(sender)

		sort = [(k, results[k]) for k in sorted(results, key=results.get, reverse=True)]
		return sort

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Extract all the senders from a mbox file and output them into a csv file sorted by number of emails sent")
	parser.add_argument("-f", dest="filename", help="MBox file to read")
	parser.add_argument("-d", dest="output", help="Output CSV file")
	args = parser.parse_args()

	processor = MailBoxDataProcessor(args.filename)
	vals = processor.run()
	csvfile = csv.writer(open(args.output, "wb"))
	for k, v in vals:
		csvfile.writerow([k, v])
