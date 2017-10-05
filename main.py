from billogram_api import *
from pyPdf import PdfFileWriter, PdfFileReader

import base64

api = BillogramAPI(
	'2519-T7ztRFnQ',
	'3524023190713a62d1d35c7292bb9f7c',
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
			# pdf_input = PdfFileReader(pdf)
			# pdf_output = PdfFileWriter(pdf_input)
			# out_put_stream = file("billogram-invoice.pdf", "wb")
			# pdf_output.write(out_put_stream)
			# out_put_stream.close()
			
			# pdf_string = pdf_string.encode('base64')
			# pdf = base64.decodestring(pdf_string)

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
		




# billogram = api.billogram.create_and_send({
#     'customer': {'customer_no': 1},
#     'items': [
#         {
#             'item_no': '2', 'count': 6
#         }, {
#             'title': 'Work', 
#             'unit': 'hour',
#             'vat': 25, 
#             'price': 300,
#             'count': 2.50
#         }
#     ]
# }, 'Email')
# # print the OCR number
# print billogram.ocr_number