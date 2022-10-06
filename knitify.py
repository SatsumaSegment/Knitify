import os
import time
import PIL.Image
import keyboard
import PySimpleGUI as sg
from itertools import groupby
from screeninfo import get_monitors

#Contrast variables
chars1 = ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
chars2 = ["#", "#", ".", ".", ".", ".", ".", ".", ".", ".", "."]
chars3 = ["#", "#", "#", ".", ".", ".", ".", ".", ".", ".", "."]
chars4 = ["#", "#", "#", "#", ".", ".", ".", ".", ".", ".", "."]
chars5 = ["#", "#", "#", "#", "#", ".", ".", ".", ".", ".", "."]
chars6 = ["#", "#", "#", "#", "#", "#", ".", ".", ".", ".", "."]
chars7 = ["#", "#", "#", "#", "#", "#", "#", ".", ".", ".", "."]
chars8 = ["#", "#", "#", "#", "#", "#", "#", "#", ".", ".", "."]
chars9 = ["#", "#", "#", "#", "#", "#", "#", "#", "#", ".", "."]
chars10 = ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "."]
chars11 = ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]

#Get the screen size, store in screen_width & screen_height
def screen_size():
      global screen_width
      global screen_height
      
      for m in get_monitors():
            lst = str(m)

      with open('screen.txt','w') as f:
            f.write(lst)
      with open('screen.txt','r') as f:
            text = f.read()
      os.remove('screen.txt')
      text=text.split()
      text=str(text[4:6])
      numstr=""
      for m in text:
            if m.isdigit():
                  numstr=numstr+m

      screen_width = int(numstr[:-3]) 
      screen_height = int(numstr[-3:]) 


      print(text)
      print(screen_width)
      print(screen_height)


def main_window():
      #Set program theme and layout
      sg.theme('greenmono')

      layout = [
            [sg.Text("Use this program to convert a black and white image into a double-knit template.", background_color='#EBFFD5')],
            [sg.Text("If your image doesn't display as desired, adjusting the contrast might help.", background_color='#EBFFD5')],
            [sg. FileBrowse('Upload image', key='-IMAGE-', button_color=('#171414','#FFF9D9')), sg.InputText(key='-IMAGEPATH-')],
            [sg.Text("Enter the size you'd like in # of stitches", background_color='#EBFFD5')],
            [sg.Text("Length:", background_color='#EBFFD5'), sg.InputText(size=20,key='-LENGTH-'), sg.Text("Width:", background_color='#EBFFD5'), sg.InputText(size=20,key='-WIDTH-')],
            [sg.Text("Contrast:", background_color='#EBFFD5'), sg.Slider(range=(1,11), default_value=6, orientation='h', key='-CONTRAST-', background_color='#EBFFD5', trough_color='#FFF9D9')],
            [sg.Button('Knitify', button_color=('#171414','#FFF9D9')), sg.ProgressBar(50,size=35, orientation='h', key='-BAR-', border_width=6, bar_color=('#FFF9D9', '#EBFFD5'))]
            ]

      window = sg.Window('Knitify V2.0', layout, background_color='#EBFFD5')
            
      while True:
            event, values = window.read()
            window['-IMAGEPATH-'].update(values['-IMAGE-'])

            #Get contrast and file path variables
            con = int(values['-CONTRAST-'])
            imagepath = values['-IMAGEPATH-']

            if con == 1:
                  contrast = chars1
            elif con ==2:
                  contrast = chars2
            elif con ==3:
                  contrast = chars3
            elif con ==4:
                  contrast = chars4
            elif con ==5:
                  contrast = chars5
            elif con ==6:
                  contrast = chars6
            elif con ==7:
                  contrast = chars7
            elif con ==8:
                  contrast = chars8
            elif con ==9:
                  contrast = chars9
            elif con ==10:
                  contrast = chars10
            elif con ==11:
                  contrast = chars11

            if event == sg.WIN_CLOSED:
                  break

            if event == 'Knitify':
                  global line_count
                  line_count = values['-LENGTH-']
                  #Check if image path and size are valid before acting
                  if os.path.exists(imagepath):
                        if int(values['-WIDTH-']) >= 0 and int(values['-LENGTH-']) >= 0:
                              
                              #Delete old file if present
                              if os.path.exists('KnitMe.txt'):
                                    os.remove('KnitMe.txt')

                              #Create ASCII Image
                              image = PIL.Image.open(imagepath)
                              width, height = image.size
                              aspect_ratio = height/width
                              #Get user to enter desired width and height (in stitches) of output image
                              new_width = int(values['-WIDTH-'])
                              new_height = int(values['-LENGTH-'])
                              #Resize and convert image to ASCII
                              image = image.resize((int(new_width), int(new_height)))
                              image = image.convert('L')
                              pixels = image.getdata()
                              new_pixels = [contrast[pixel//25] for pixel in pixels]
                              new_pixels = ''.join(new_pixels)
                              new_pixels_count = len(new_pixels)
                              ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
                              ascii_image = "\n".join(ascii_image)
                              #Save ASCII file
                              with open('tempimage.txt','w') as f:
                                    f.write(ascii_image)
                              with open('tempimage.txt','r') as f:
                                    lines = f.read()
                              with open('image.txt','w') as f:
                                    f.write(lines[::-1])

                              os.remove('tempimage.txt')
                              #Create numbers and KnitMe files
                              with open('image.txt', 'r') as f:
                                    for line in map(lambda l: l.strip(), f):
                                          runs = [sum(1 for _ in g) for _, g in groupby(line)]
                                          x = f"{line} {' '.join(map(str, runs))}"
                                          with open('KnitMe.txt','a') as z:
                                                z.write(x+'\n')
                                          with open('tempdata.txt', 'a') as y:
                                                y.write(str(runs)+'\n')
                              #Format data file
                              with open('tempdata.txt', 'r') as f:
                                    filedata = f.read()
                              filedata = filedata.replace(',', ']').replace(' ', '[')
                              with open('data.txt', 'w') as f:
                                    f.write(filedata)
                              os.remove('tempdata.txt')

                              #Progress bar bit
                              progbar = 1
                              for i in range(8):
                                    window['-BAR-'].update_bar(progbar)
                                    progbar = progbar+progbar
                                    time.sleep(0.2)
                              window['-BAR-'].update_bar(0)
                              knitify_window()

      window.close()

def knitify_window():
      #Iteration bits
      x=0
      #Store text and numbers as lists and strings
      with open('image.txt', 'r') as f:
            text = f.read()
      with open('data.txt','r') as f:
            data = f.read()
      with open('data.txt','r') as f:
            data_lines = f.readlines()
      with open('image.txt','r') as f:
            text_lines = f.readlines()

      #Get longest line from numbers and text
      text_max = max(open('image.txt'),key=len)
      data_max = max(open('data.txt'),key=len)

      #Use screen size to determine width of text boxes
      text_max = int(len(text_max))
      data_max = int(len(data_max))
      text_box_size = text_max
      data_box_size = data_max
      print(data_max)
      print(text_max)
      if text_max > 50:
            text_box_size = int(screen_width/5)
            print(text_box_size)
      else:
            text_box_size = text_max
      if data_max > 50:
            data_box_size = int(screen_width/10)
            print(data_box_size)
      else:
            data_box_size = data_max
      
    #Set layout of window  and maximize
      layout = [
            [sg.Multiline(size=text_box_size, expand_y=True, default_text=text, font='Consolas', key='-TEXT-', background_color='#FFF9D9', horizontal_scroll = True, disabled=True),
            sg.Multiline(size=data_box_size, expand_y=True, default_text=data, font='Consolas', key='-DATA-', background_color='#FFF9D9', horizontal_scroll = True, disabled=True), sg.Button('<--', expand_y=True, expand_x=True, button_color=('#171414','#FFF9D9')),
            sg.Button('-->', expand_y=True, expand_x=True,  button_color=('#171414','#FFF9D9'))]
            ]

      window = sg.Window('Knitified', layout, background_color='#EBFFD5',finalize=True)
      window.Maximize()
      
      while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                  break

            if event == '<--':
                  return

            if event == '-->':
                  if x < 1:
                        window['-DATA-'].update('')
                        window['-TEXT-'].update('')
                  window['-DATA-'].update(data_lines[x], background_color_for_value='#C1FCFF' , append=True)
                  window['-TEXT-'].update(text_lines[x], background_color_for_value='#C1FCFF' , append=True)
                  x=x+1

      #REMEMBER SCREEN SIZE.
      #TEXT BOXES DEVIDED BY SCREEN
      #UNLESS IMAGE SMALL ENOUGH (< ~ 50)

            #UP COUNTER UP FOR HIGHLIGHT LINES
            #DOWN COUNTER TO GET FROM HIGHLIGHT LINE TO LAST LINE. TO TELL HOW MANY LINES LEFT
                  #STARTS AT MAX LINES, COUNTS DOWN IN FOR LOOP AND RESETS FOR EACH BUTTON PRESS
            # 10 LINES - HIGHLIGHT ON LINE 5 H[5] - REST = [5:10] 
            
            ##### TRY READLINES()#####
      window.close()

screen_size()                              
main_window()

