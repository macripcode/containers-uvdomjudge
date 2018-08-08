import xlsxwriter

workbook = xlsxwriter.Workbook('doc_properties.xlsx')
worksheet = workbook.add_worksheet()

workbook.set_properties({
    'title':    'This is an example spreadsheet',
    'subject':  'With document properties',
    'author':   'John McNamara',
    'manager':  'Dr. Heinz Doofenshmirtz',
    'company':  'of Wolves',
    'category': 'Example spreadsheets',
    'keywords': 'Sample, Example, Properties',
    'comments': 'Created with Python and XlsxWriter',
    'status':   'Quo',
})

worksheet.set_column('A:A', 70)
worksheet.write('A1', "Select 'Workbook Properties' to see properties.")

workbook.close()