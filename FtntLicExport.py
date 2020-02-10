import eel, PyPDF2, re, zipfile, os
from tkinter import filedialog
from tkinter import *


# Set web files folder and optionally specify which file types to check for eel.expose()
#   *Default allowed_extensions are: ['.js', '.html', '.txt', '.htm', '.xhtml']
eel.init('web', allowed_extensions=['.js', '.html'])

@eel.expose
def getlicencefromfolder(folder_name):
    licresult = ""
    licresulthtml = ""
    for filename in os.listdir(folder_name):
        if filename.endswith(".zip"):

            zipcontents = zipfile.ZipFile(folder_name + "/" + filename, "r")

            for evalpdf in zipcontents.namelist():
                data = zipcontents.open(evalpdf, 'r')

                eval_reg = ''
                eval_sn = ''
                eval_sku = ''

                pdfReader = PyPDF2.PdfFileReader(data)

                num_pages = pdfReader.numPages
                count = 0
                text = ""

                while count < num_pages:
                    pageObj = pdfReader.getPage(count)
                    count += 1
                    text += pageObj.extractText()

                regcode = re.search("Registration Code\s\s\s:\s\s(.....-.....-.....-.....-......)", text)
                partcode = re.search("days\s\s\s\s\s\s?(\w\w.*?\d\d\d\d+)\w", text)
                eval_reg = regcode.group(1)
                partcode_filter = partcode.group(1)

                eval_sn = evalpdf.strip('.pdf')
                eval_sku = partcode_filter.replace(eval_sn, '')

                print(eval_sku + "\t" + eval_sn + "\t" + eval_reg)
                licresult += eval_sku + "\t" + eval_sn + "\t" + eval_reg + "\n"
                licresulthtml += "<tr><td>" + eval_sku + "</td><td>" + eval_sn + "</td><td>" + eval_reg + "</td></tr>"

    if licresult == "":
        licresult = "No licence codes found."
        licresulthtml = "<tr><td colspan=3>No licence codes found.</td></tr>"

    #return_html = "<h3>Licence Codes</h3><table border=1><tr><th>SKU&nbsp;&nbsp;</th><th>Serial No.&nbsp;&nbsp;</th><th>Registration Code&nbsp;&nbsp;</th></tr>" + licresulthtml + "</table><br><br><textarea readonly rows=\"10\" id=\"jsonexport\" class=\"form-control\" style=\"min-width: 100%\">" + licresult + "</textarea><br/>\n<a href=app.html>Return</a>"
    return_html = "<h3>Licence Codes</h3><br><textarea readonly rows=\"10\" id=\"jsonexport\" class=\"form-control\" style=\"min-width: 100%\">" + licresult + "</textarea><br/>\n<a href=app.html>Return</a>"


    eel.pageupdate(return_html)


@eel.expose
def btn_getfoldername():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    foldername = filedialog.askdirectory(initialdir="/", title="Select Folder")
    root.update()  # to make dialog close on MacOS
    print(foldername)

    return foldername




eel.start('app.html', size=(790, 500), disable_cache=True)
