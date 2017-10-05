import base64
import json
from billogram_api import *

# Import config file
with open("config.json") as f: 
	config_file = json.load(f)

api = BillogramAPI(
	config_file['username'],
	config_file['password'],
	api_base='https://sandbox.billogram.com/api/v2'
)

query = api.billogram.query()
query.filter_state_any('Unpaid', 'Credited')

bgs = query.get_page(1)
bg = bgs[0]

bg.refresh()

for ev in bg['events'] :
	if ev['data'] and 'letter_id' in ev['data'] :
		try :
			pdf_string = bg.get_invoice_pdf(letter_id=ev['data']['letter_id'])

			with open("test1.pdf", "wb") as f: 
				f.write(pdf_string)

		except BillogramExceptions.ObjectNotAvailableYetError :
			# pdf not created yet
			print "PDF not created yet"
			pass
		except BillogramExceptions.ObjectNotFoundError :
			# pdf was not found
			print "PDF was not found"
			pass
