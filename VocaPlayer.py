

import tkinter as tk
import tkinter.messagebox as msg
from tkinter import IntVar
from tkinter import filedialog

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors

#####################################################################################
#
#	Copyright (c) 2000-2018, ReportLab Inc.
#	All rights reserved.
#
#	Redistribution and use in source and binary forms, with or without modification,
#	are permitted provided that the following conditions are met:
#
#		*	Redistributions of source code must retain the above copyright notice,
#			this list of conditions and the following disclaimer. 
#		*	Redistributions in binary form must reproduce the above copyright notice,
#			this list of conditions and the following disclaimer in the documentation
#			and/or other materials provided with the distribution. 
#		*	Neither the name of the company nor the names of its contributors may be
#			used to endorse or promote products derived from this software without
#			specific prior written permission. 
#
#	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#	ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#	WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#	IN NO EVENT SHALL THE OFFICERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#	INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
#	TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#	OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
#	IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#	IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#	SUCH DAMAGE.
#
#####################################################################################


import csv
import os
import random


class ListData:

    def __init__(self):
        self.setData()

    def setData(self):
        root = tk.Tk()
        root.withdraw()
        filetype=[("csv","*.csv")]    
        openpath = filedialog.askopenfilename(initialdir=".",filetypes=filetype)
        root.destroy() 
        with open(openpath,"r") as f:
            reader = csv.reader(f)
            self.data = [ e for e in reader ]

    def setParagraph(self,content):
        style = ParagraphStyle(name='Normal', fontName=fontname)
        text = Paragraph(content,style)
        return text

    def setSelectData(self,n):
        #this method must be called before the colling of getHideData
        self.selectdata = random.sample(self.data,n)

    def getHideData(self,col):
        hidedata =[]
        for row in self.selectdata:
            hidedata.append(["" if i==col else row[i] for i in range(len(row))])        
        return hidedata


#-----------------------------write to pdf----------------------------------


def writeContent(data,savefilename):
    header = [['Vocabulary_test','Name:','Point:']]
    header[0] = list(map(listdata.setParagraph, header[0]))
    head = Table(header,colWidths=60*mm)
    head.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                    ("ALIGN", (0,0), (-1,-1), "LEFT"),
                    ('GRID', (0,0), (-1,-1), 0.25, colors.black),
                    ])
    for i in range(len(data)):
        data[i] = list(map(listdata.setParagraph, data[i]))
    table = Table(data, colWidths=80*mm)
    table.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                    ("ALIGN", (0,0), (-1,-1), "LEFT"),
                    ('GRID', (0,0), (-1,-1), 0.25, colors.black),
                    ])
    doc = SimpleDocTemplate(savefilename)
    doc.build([head,Spacer(1,5*mm),table])


def controller():
    filetype=[("pdf","*.pdf")]   
    savepath = filedialog.asksaveasfilename(initialdir=".",filetypes=filetype)
    savepath = os.path.splitext(savepath)
    savefilenamealldata = savepath[0] + '_all.pdf'
    savefilenamehidecol0 = savepath[0] + '_hidecol0.pdf'
    savefilenamehidecol1 = savepath[0] + '_hidecol1.pdf'
    
    n = quiz_size.get()
    print(n)
    listdata.setSelectData(n)
    alldata = listdata.selectdata
    hidecol0 = listdata.getHideData(0)
    hidecol1 = listdata.getHideData(1)
    writeContent(alldata,savefilenamealldata)
    writeContent(hidecol0,savefilenamehidecol0)
    writeContent(hidecol1,savefilenamehidecol1)

    msg.showinfo('informatin','終わりました!')


def renewalData(scale):
    #in order to update to=len(listdata.data)
    scale.destroy()
    listdata.setData()
    scale   = tk.Scale(base, variable = quiz_size,label = '問題数' , orient= 'h',
                            from_=1, to=len(listdata.data), width = 20, length = 200)
    scale.pack()



if __name__ == '__main__':
    
    listdata = ListData()

    fontname = "HeiseiKakuGo-W5"
    pdfmetrics.registerFont(UnicodeCIDFont(fontname))

    base = tk.Tk()
    base.title('VocaPlayer')
    base.geometry('400x200')

    tk.Button(base,text = '一問一答問題を作って!',width=30, command = lambda: controller()).pack()

    quiz_size = IntVar()
    scale   = tk.Scale(base, variable = quiz_size,label = '問題数' , orient= 'h',
                            from_=1, to=len(listdata.data), width = 20, length = 200)
    scale.pack()
    

    men = tk.Menu(base) 
    base.config(menu=men) 
    pulldown = tk.Menu(base) 
    men.add_cascade(label='データ', menu=pulldown) 
    pulldown.add_command(label='別のデータを使用する', command=lambda: renewalData(scale)) 

    base.mainloop()

