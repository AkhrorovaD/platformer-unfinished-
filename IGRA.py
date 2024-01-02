from tkinter import *
import random
import time
class Kord:
    def __init__(self,x1=0,y1=0,x2=0,y2=0):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
    def po_x(obj_1,obj_2):
        if (obj_1.x1>obj_2.x1 and obj_1.x1<obj_2.x2) or (obj_1.x2>obj_2.x1 and obj_1.x2<obj_2.x2):
            return True
        else:
            return False

    def po_y(obj_1,obj_2):
        if (obj_1.y1>obj_2.y1 and obj_1.y1<obj_2.y2) or (obj_1.y2>obj_2.y1 and obj_1.y2<obj_2.y2):
            return True
        else:
            return False

    def levo (obj_1,obj_2):
        if po_y(obj_1,obj_2):
            if obj_1.x1<=obj_2.x2 and obj_1.x1>=obj_2.x1:
                return True
        return False
    
    def pravo (obj_1,obj_2):
        if po_y(obj_1,obj_2):
            if obj_1.x2<=obj_2.x2 and obj_1.x2>=obj_2.x1:
                return True
        return False
    
    def verx (obj_1,obj_2):
        if po_x(obj_1,obj_2):
            if obj_1.y1>=obj_2.y1 and obj_1.y1<=obj_2.y2:
                return True
        return False

    def vniz (obj_1,obj_2):
        if po_x(obj_1,obj_2):
            y_new=obj_1.y2+y
            if y_new>=obj_2.y1 and y_new<=obj_2.y2:
                return True
        return False
    
class Igra:
    def __init__(self):
        self.HARDMODE=False
        self.tk=Tk()
        self.tk.title("IGRA")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost",1)
        self.w=1200
        self.h=700
        self.bg=PhotoImage(file="priroda.gif")
        self.can=Canvas(self.tk,width=self.w,height=self.h,highlightthickness=0)
        self.can.pack()
        self.can.create_image(0,0,image=self.bg,anchor='nw')
        self.tk.update()
        self.sprayts=[]
        self.beg=True

    def mainloop(self):
        while 1:
            if self.beg==True:
                for sprite in self.sprayts:
                    sprite.move()
                self.tk.update_idletasks()
                self.tk.update()
                time.sleep(0.012)
class Sprayt:
    def __init__(self,igra):
        self.igra=igra
        self.konec=False
        self.kordin=None
    def move(self):
        pass
    def kord(self):
        return self.kordin
        
class Sprite_uroda(Sprayt):
    def __init__(self,igra):
        Sprayt.__init__(self,igra)
        self.levo=[PhotoImage(file="urod2.gif"),PhotoImage(file="levo_1.gif"),PhotoImage(file="levo_2.gif"),PhotoImage(file="levo_3.gif")]
        self.pravo=[PhotoImage(file="urod1.gif"),PhotoImage(file="pravo_1.gif"),PhotoImage(file="pravo_2.gif"),PhotoImage(file="pravo_3.gif")]
        self.image=igra.can.create_image(30,self.igra.h-300,image=self.pravo[0],anchor='nw')
        self.x=0
        self.y=0
        igra.can.bind_all('<KeyPress-Left>',self.nalevo)
        igra.can.bind_all('<KeyPress-Right>',self.napravo)
        igra.can.bind_all('<space>',self.skok)
        self.cur_image=0
        self.image_add=1
        self.skok_count=0
        self.kordin=Kord()
        self.last_time=time.time()
    def nalevo(self,evt):
        if self.y==0:
            self.x=-2
            
    def napravo(self,evt):
        if self.y==0:
            self.x=2

    def skok(self,evt):
        if self.y==0:
            self.y=-6
            self.skok_count=0

    def animate(self):
        if self.x!=0 and self.y==0:
            if time.time()-self.last_time>0.1:
                self.last_time=time.time()
                self.cur_image+=self.image_add
                if self.cur_image>=3:
                    self.image_add=-1
                if self.cur_image<=1:
                    self.image_add=1
        if self.x<0:
            if self.y!=0:
                self.igra.can.itemconfig(self.image,image=self.levo[3])
            else:
                self.igra.can.itemconfig(self.image,image=self.levo[self.cur_image])
        elif self.x>0:
            if self.y!=0:
                self.igra.can.itemconfig(self.image,image=self.pravo[3])
            else:
                self.igra.can.itemconfig(self.image,image=self.pravo[self.cur_image])
    def kord(self):
        xy=self.igra.can.coords(self.image)
        self.kordin.x1=xy[0]
        self.kordin.y1=xy[1]
        self.kordin.x2=xy[0]+148
        self.kordin.y2=xy[1]+234
        return self.kordin

    def move(self):
        self.animate()
        if self.y<0:
            self.skok_count+=1
            if self.skok_count>20:
                self.y=6
        if self.y>0:
            self.skok_count-=1
        ko=self.kord()
        left=True
        right=True
        top=True
        bottom=True
        falling=True
        if self.y>0 and ko.y2>=self.igra.h-66:
            self.y=0
            bottom=False
        elif self.y<0 and ko.y1<=0:
            self.y=0
            top=False
        if self.x>0 and ko.x2>=self.igra.w:
            self.x=0
            right=False
        elif self.x<0 and ko.x1<=0:
            self.x=0
            left=False
        for sprite in self.igra.sprayts:
            if sprite ==self:
                continue
            sprite_co=sprite.kord()
            if top and self.y<0 and verx(ko,sprite_co):
               self.y=-self.y
               top=False
            if bottom and ko.x2<=200 and ko.x1>=800 and self.y>0 and vniz(self.y,ko,sprite_co):
                self.y=sprite_co.y1-ko.y2
                if self.y<0:
                    self.y=0
                bottom=False
                top=False
            if bottom and falling and self.y==0 and ko.y2<self.igra.h-66 and ko.x2<=200 or ko.x1>=800 and vniz(1,ko,sprite_co):
                falling=False
            if left and self.x<0 and levo(ko,sprite_co):
                self.x=0
                left=False
            if right and self.x>0 and pravo(ko,sprite_co):
                self.x=0
                right=False
        if bottom and falling and self.y==0 and ko.y2<=self.igra.h-66:
            self.y=6
        self.igra.can.move(self.image,self.x,self.y)
            
igra=Igra()
urod_poyavis=Sprite_uroda(igra)
igra.sprayts.append(urod_poyavis)
igra.mainloop()
