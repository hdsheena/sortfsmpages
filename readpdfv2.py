from subprocess import call, check_output
import glob
filename_sections = {}
files_needing_names = {}

section_number = "6"

for pdf_file in glob.glob('*ocr.pdf'): 
    #print pdf_file
    output = check_output(['/home/home/.local/bin/pdf2txt.py', pdf_file])
    start = output.find(section_number)
    if output[start+1] == ")":
        from_bracket = output[start+1:start+15]
        #print from_bracket
        after_bracket = from_bracket.find(section_number)     
        #print after_bracket, "After bracket" 
        correct_start = start + after_bracket + 1
       # print output[start+after_bracket:start+after_bracket+8]
    else:
        correct_start = start
    end = correct_start+8
    filename = output[correct_start:end]
    print filename, pdf_file
    files_needing_names[filename] = pdf_file

def put_into_list(newlist,unit, number):
    """
Take the pieces of the file identifier and break them into a neat list of one id per list item
    """
    if unit.isdigit():
            newlist.insert(number, unit)
    elif unit.isalpha():
            newlist.insert(number, unit)
    else:
            parse_more = list(unit)
            for item in parse_more:
                newlist.insert(number, item)
                number += 1
    return newlist, number

def remove_blanks(list_of_items):
    """
Take the list and remove any blank entries
    """
    for item in list_of_items:
        if item.isalnum():
            pass
        else:
            list_of_items.remove(item)
    return list_of_items

bad_ocr = []
for filenames in files_needing_names.keys():
#need to check that the filename here is of the right format before doing this
    if "-" not in filenames:
        if "~" not in filenames:
            print "This file is not OCR'd correctly: " + filenames
            bad_ocr.append(files_needing_names[filenames])
            continue
    units = filenames.split("-")
    #print units
    number = -1
    parse_more = []
    newlist = []
    for unit in units:
	number+=1
        newlist, number = put_into_list(newlist, unit, number)
        #print parse_more

    sections = remove_blanks(newlist)
    #sections.append(parse_more)
    #print sections
    filename_sections[filenames] = sections

#print files_needing_names
for key in filename_sections.keys():
    print key, filename_sections[key]
print "need to re OCR"
print bad_ocr
