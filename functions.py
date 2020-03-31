from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io
import os
import shutil
from PyPDF2 import PdfFileMerger
from PyPDF2 import PdfFileReader, PdfFileWriter


def scan_folder(parent, keyword):
    lista = []
    # iterate over all the files in directory 'parent'
    for file_name in os.listdir(parent):
        resource_manager = PDFResourceManager()
        handle = io.StringIO()
        converter = TextConverter(resource_manager, handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        if file_name.endswith(".pdf"):
            # if it's a txt file, print its name (or do whatever you want)
            arquivo = open(parent + "/" + file_name, 'rb')
            with arquivo as fh:

                for page in PDFPage.get_pages(fh,
                                              caching=True,
                                              check_extractable=True):
                    page_interpreter.process_page(page)
                text = handle.getvalue()
                if (text.find(keyword) != -1):
                    # print(file_name + " TEEM")
                    lista.append(parent + "/" + file_name)
                # else:
                # print(file_name + " NAOOOO")
                converter.close()
                handle.close()
        else:
            current_path = "".join((parent, "/", file_name))
            if os.path.isdir(current_path):
                # if we're checking a sub-directory, recall this method
                scan_folder(current_path)
    return lista


def merger(output_path, input_paths):
    pdf_merger = PdfFileMerger()
    file_handles = []

    for path in input_paths:
        pdf_merger.append(path)

    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)


def searchPDF(parent, keyword):
    lista = []
    # iterate over all the files in directory 'parent'
    for file_name in parent:
        resource_manager = PDFResourceManager()
        handle = io.StringIO()
        converter = TextConverter(resource_manager, handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        arquivo = open(file_name, 'rb')
        with arquivo as fh:
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                page_interpreter.process_page(page)
                text = handle.getvalue()
                if (text.find(keyword) != -1):
                    # print(file_name + " TEEM")
                    lista.append(file_name)
                # else:
                # print("NAO")
        converter.close()
        handle.close()
    return lista


def splitter(path, output_folder):
    for x in path:
        fname = os.path.splitext(os.path.basename(x))[0]
        pdf = PdfFileReader(x)
        for page in range(pdf.getNumPages()):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))
            pages = page + 1
            if page >= 99:
                pagename = str(pages)
            elif page >= 9:
                pagename = "0" + str(pages)
            else:
                pagename = "00" + str(pages)
            output_filename = output_folder + '/{}_page_{}.pdf'.format(
                fname, pagename)
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)
            # print('Created: {}'.format(output_filename))


def splitterCustom(path, output_folder, doublepageslist,originalfile):
    for x in path:
        fname = os.path.splitext(os.path.basename(x))[0]
        pdf = PdfFileReader(x)
        print(x)
        filenumber = find_between(x, "_file_", ".pdf")
        if filenumber not in originalfile:
            doublepageslist2 = []
        else:
            doublepageslist2 = doublepageslist
        b = True
        for page in range(pdf.getNumPages()):
            pagenamemerged = str(page + 1) + ";" + filenumber
            print(pagenamemerged)
            pdf_writer = PdfFileWriter()
            if b:
                if pagenamemerged not in doublepageslist2:
                    pdf_writer.addPage(pdf.getPage(page))
                    pages = page + 1
                    if page >= 99:
                        pagename = str(pages)
                    elif page >= 9:
                        pagename = "0" + str(pages)
                    else:
                        pagename = "00" + str(pages)
                    output_filename = output_folder + '/{}_page_{}.pdf'.format(fname, pagename)
                    with open(output_filename, 'wb') as out:
                        pdf_writer.write(out)
                    # print('Created: {}'.format(output_filename))
                    b = True
                else:
                    pdf_writer.addPage(pdf.getPage(page))
                    pdf_writer.addPage(pdf.getPage(page + 1))
                    pages = page + 1
                    if page >= 99:
                        pagename = str(pages)
                    elif page >= 9:
                        pagename = "0" + str(pages)
                    else:
                        pagename = "00" + str(pages)
                    output_filename = output_folder + '/{}_page_{}.pdf'.format(
                        fname, pagename)
                    with open(output_filename, 'wb') as out:
                        pdf_writer.write(out)
                    # print('Created: {}'.format(output_filename))
                    b = False
            else:
                b = True


def splitterNew(path, output_folder):
    for x in path:
        name = os.path.splitext(os.path.basename(x))[0]
        print(*name)
        pdf = PdfFileReader(x)
        for page in range(pdf.getNumPages()):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))
            output_filename = output_folder + '/{}_{}.pdf'.format(
                page + 1, name)
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)
            # print('Created: {}'.format(output_filename))


def list_files_mac(dir):
    names = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.pdf'):
                names.append(dir + "/" + file)
    return names


def list_files_win(dir):
    names = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.pdf'):
                names.append(dir + "/" + file)
    return names


def list_files_walk(directory):
    fu = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames if
          os.path.splitext(f)[1].lower() == '.pdf']
    return (fu)


def newScan(parent):
    lista = []
    f = open("designs.txt", "w+")
    g = open("paths.txt", "w+")
    # iterate over all the files in directory 'parent'
    for file_name in parent:
        resource_manager = PDFResourceManager()
        handle = io.StringIO()
        converter = TextConverter(resource_manager, handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        arquivo = open(file_name, 'rb')
        with arquivo as fh:
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                page_interpreter.process_page(page)
                text = handle.getvalue()
                word = find_between(text, "SKUPrice1", "$")
                print(word)
                # number = has_sequence(word)
                # stringnumber = ''.join(map(str, number))
                # artwork = find_between(word,"1",stringnumber)

                f.write(word + "\n")
                g.write(file_name + "\n")
        converter.close()
        handle.close()
    f.close()
    g.close()
    return lista


def scanDoublePages(parent, galleryprices, dailyprices):
    daily = open("daily.txt", "w+")
    gal = open("gallery.txt", "w+")
    sweet = open("sweet.txt", "w+")
    duplicatestest = open("duplicatestest.txt", "w+")
    number = 0
    numberlist = []
    originalfile = []
    folder = "temp"
    cleanFolder(folder)
    # listing the files inside the folder
    parentnew = list_files_walk(parent)
    # creating a temporary folder
    os.mkdir(folder)
    # splitting the temporary files
    splitter(parentnew, folder)
    # getting the temporary files
    parentnew2 = list_files_walk(folder)
    # sorting the files by name
    parentnew2.sort()
    # iterate over all the files in directory 'parent'
    for file_name in parentnew2:
        resource_manager = PDFResourceManager()
        handle = io.StringIO()
        converter = TextConverter(resource_manager, handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        arquivo = open(file_name, 'rb')
        if "page_001.pdf" in file_name:
            number = 0
        with arquivo as fh:
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                booleangal = True
                booleanSweet = True
                page_interpreter.process_page(page)
                text = handle.getvalue()
                text = text[:-1]
                text = text + "¬¬¬"
                #print(text)
                # searching the reference number
                search = find_between(text, "#", "Order")
                # searching the order number
                search2 = find_between(text, "# ", "Order Date")
                # Searching the design name
                name = find_between(text, "SKUPrice1", "$")
                # Prices
                price = find_between(text, name, ",")
                # Products
                products = find_between(text, "SKUPrice1", "¬¬¬")
                #print(products)
                originalfilenumber = find_between(file_name, "_file_", "_page")
                print(originalfilenumber)
                if search == "":
                    numberlist.append(str(number) + ";" + originalfilenumber)
                    originalfile.append(originalfilenumber)
                    # print(result[number-1])
                    # f.write(result[number - 1] + "\n")
                else:
                    duplicatestest.write(search2 + "\n")
                    for daprices in dailyprices:
                        if products.find(daprices) != -1:
                            print(search2 + " Daily Shirt")
                            booleangal = False
                            daily.write(name + "^" + file_name + "^" + search2 + "\n")
                            break
                    if booleangal:
                        for gaprices in galleryprices:
                            if products.find(gaprices) != -1:
                                print(search2 + " Gallery Shirt")
                                gal.write(name + "^" + file_name + "^" + search2 + "\n")
                                booleanSweet = False
                                break
                        if booleanSweet:
                            sweet.write(name + "^" + file_name + "^" + search2 + "\n")
                            print(search2 + " Sweet Deal")
                number = number + 1
        converter.close()
        handle.close()
    daily.close()
    gal.close()
    duplicatestest.close()
    sweet.close()
    cleanFolder(folder)
    print(originalfile)
    print("Files with double pages: ")
    print(numberlist)
    os.mkdir(folder)
    splitterCustom(parentnew, folder, numberlist,originalfile)


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def has_sequence(s):
    val = []
    number = []
    length = len(s)
    for x in range(length):
        try:
            prov = int(s[x])
            val.append(prov)

        except ValueError:
            val.append("%")

    for x in range(length):
        if val[x] == "%":
            1
        else:
            if val[x + 1] == "%":
                1
            else:
                number.append(val[x])
    return number


def sortFiles(file_name):
    f = open(file_name + ".txt", "r")
    contents = f.readlines()
    contents.sort()
    with open(file_name + "_sorted.txt", "w+") as g:
        for item in contents:
            g.write(item)
    f.close()
    g.close()


def cleanFolder(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def checkIfDuplicates(listOfElems):
    for elem in listOfElems:
        if listOfElems.count(elem) > 1:
            return True
    return False