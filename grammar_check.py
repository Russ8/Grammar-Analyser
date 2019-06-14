import grammar_check
import xml.etree.ElementTree as etree
import csv
import sys


tool = grammar_check.LanguageTool('en-GB')

def number_grammer_errors(text) :
    
    matches = tool.check(text)
    return len(matches)


def extract_text_only(text) :
    ret = ''
    inside_paragraph = False
    level = 0
    i = 0
    culled_text = ""
    while i < len(text) :
        if text[i] == '<':
            i=i+1
            if text[i] == 'p' :
                inside_paragraph = True
            elif text[i] == '/' :
                i=i+1
                if text[i] == 'p' :
                    inside_paragraph = False
                else :
                    level=level-1
            else:
                level=level+1
            while text[i] != '>' and i < len(text) :
                i=i+1
                #sys.stdout.write('.')
        if inside_paragraph == True and level == 0 and text[i] != '>':
            culled_text += text[i]
        i=i+1
    return culled_text

counter = 0
f = open('testcsv.csv','a')
#f.write('index,id,length,num_errors,errors_per_100_chars,score,num_answers,accepted_answer\n')
skip = int(sys.argv[1]) * 500
end = skip + 500
print skip
for _, elem in etree.iterparse("Posts.xml"):
    counter = counter + 1
    if counter < skip :
        #print counter, skip
        counter = counter + 1
        continue
    if counter > end :
        break
    #print('questions included')
    print(counter)
    #print('accepted ansewer id: ')
    accepted_answer = 0
    if 'AcceptedAnswerId' in elem.attrib :
        accepted_answer = 1
        #print('question has accepted answer')
    #else :
        #print('no accepted answer')
    
    question = elem.attrib['Body']
    
    Id = -1
    if 'Id' in elem.attrib :
        Id = elem.attrib['Id']
    
    full_text = extract_text_only(question)

    errors = number_grammer_errors(full_text)

    adj = -1
    if len(full_text) != 0 :
        print ('adj score ' + str(errors) )
        adj =  100 * errors / len(full_text)
        print (adj)
    #else :
        #print ('no body')
    qr = -1
    #print("question reputation")
    if 'Score' in elem.attrib :
        qr = elem.attrib['Score']
        #print(qr)
    #else :
        #print('no rep')
    num_answers = 0
    #print("num answers")
    if 'AnswerCount' in elem.attrib :
        num_answers = elem.attrib['AnswerCount'] 
        #print(num_answers)
    #else :
        #print ('no answers')
    #print('write')
    f.write(str(counter) + ',' + str(Id) + ',' + str(len(full_text)) + ',' + str(errors) + ',' + str(adj) + ',' + str(qr) + ',' + str(num_answers) + ',' + str(accepted_answer) + '\n')
    #print('done write')
f.close()

    



