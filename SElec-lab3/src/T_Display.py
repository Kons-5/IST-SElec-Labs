import sys
import time
import gc

DELAY_START_MS = 5000         # 5000

WIDTH = 240
HEIGHT = 135

DISPLAY_WIDTH  = 135
DISPLAY_HEIGHT = 240

print("Start of T_Display: Version 1.03")


def file_exists(filename):
    try:
        f=open(filename,'r')
        f.close()
        return(True)
    except OSError:
        return(False)


if sys.implementation.name == "micropython":

    MICROPYTHON = True
    print("MICROPYTHON")
    
    from machine import ADC,Pin,unique_id
    from ubinascii import hexlify
    import array
    from uctypes import addressof


    memoria_adc=[0]*240
    
    adc1=ADC(Pin(36))
    adc1.atten(ADC.ATTN_6DB)
    # Atenuador
    #  - Sem atenuador R1 e R5+R6+R7 caso Q1 e Q2 ao corte Fator=(R5+R6+R7)/(R1+R5+R6+R7)=0.509=1/1.97
    #  - Atenuador 1   R1 e R5+R6 caso Q1 a conduzir e Q2 ao corte, Fator=(R5+R6)/(R1+R5+R6)=0.0342=1/29.3
    #  - Atenuador 2   R1 e R5 caso Q2 a conduzir e Q1 ao corte,    Fator=R5/(R1+R5)=0.00239=1/418

    ENABLE_ATTN_1 = Pin(32, Pin.OUT)       # Atenuador 1
    ENABLE_ATTN_1.on()
    ENABLE_ATTN_2 = Pin(33, Pin.OUT)       # Atenuador 2
    ENABLE_ATTN_2.off()
    ENABLE_REFF = Pin(25, Pin.OUT)         # Atenuador 3
    ENABLE_REFF.off()
	
    import machine
    import ustruct as struct
    from prvReadBMP import prvReadBMP
    import _thread
    from machine import ADC,Pin
    import urequests as requests

	
    # commands
    ST77XX_NOP = const(0x00)
    ST77XX_SWRESET = const(0x01)
    ST77XX_RDDID = const(0x04)
    ST77XX_RDDST = const(0x09)

    ST77XX_SLPIN = const(0x10)
    ST77XX_SLPOUT = const(0x11)
    ST77XX_PTLON = const(0x12)
    ST77XX_NORON = const(0x13)

    ST77XX_INVOFF = const(0x20)
    ST77XX_INVON = const(0x21)
    ST77XX_DISPOFF = const(0x28)
    ST77XX_DISPON = const(0x29)
    ST77XX_CASET = const(0x2A)
    ST77XX_RASET = const(0x2B)
    ST77XX_RAMWR = const(0x2C)
    ST77XX_RAMRD = const(0x2E)

    ST77XX_PTLAR = const(0x30)
    ST77XX_COLMOD = const(0x3A)
    ST7789_MADCTL = const(0x36)

    ST7789_MADCTL_MY = const(0x80)
    ST7789_MADCTL_MX = const(0x40)
    ST7789_MADCTL_MV = const(0x20)
    ST7789_MADCTL_ML = const(0x10)
    ST7789_MADCTL_BGR = const(0x08)
    ST7789_MADCTL_MH = const(0x04)
    ST7789_MADCTL_RGB = const(0x00)

    ST7789_RDID1 = const(0xDA)
    ST7789_RDID2 = const(0xDB)
    ST7789_RDID3 = const(0xDC)
    ST7789_RDID4 = const(0xDD)

    ColorMode_65K = const(0x50)
    ColorMode_262K = const(0x60)
    ColorMode_12bit = const(0x03)
    ColorMode_16bit = const(0x05)
    ColorMode_18bit = const(0x06)
    ColorMode_16M = const(0x07)


    _ENCODE_PIXEL = ">H"
    _ENCODE_POS = ">HH"
    _DECODE_PIXEL = ">BBB"

    #_BUFFER_SIZE = const(256)
                               
    _BUFFER_SIZE = const(256)

    DISPLAY_WIDTH  = const(135)
    DISPLAY_HEIGHT = const(240)
    #DISPLAY_SQUARE = const(DISPLAY_WIDTH * DISPLAY_HEIGHT)
    DISPLAY_SQUARE = const(DISPLAY_WIDTH * DISPLAY_HEIGHT)
    DISPLAY_XSTART = const(52)
    DISPLAY_YSTART = const(40)

    PIN_BL   = const(0x01<<4)                      # bl
    PIN_CS   = const(0x01<<5)                      # cs
    PIN_RST  = const(0x01<<23)                     # rst
    PIN_DC   = const(0x01<<16)                     # dc
    PIN_CLK  = const(0x01<<18)                     # clk
    PIN_MOSI = const(0x01<<19)                     # mosi
    gpio_base_register=0x3FF44004
    gc.collect()

    button_clicked=0
    time_clicked=0
    time_released=0

    def threadFunction(tft):
        global button_clicked
        global time_clicked
        global time_released

        Button1=Pin(35,Pin.IN)
        Button2=Pin(0,Pin.IN)
        
        while True:
            if not Button1.value() and button_clicked==0:    # click 1
                button_clicked=1
                time_clicked=time.ticks_ms()
                time_released=0
            elif not Button2.value() and button_clicked==0:  # click 2
                button_clicked=2
                time_clicked=time.ticks_ms()
                time_released=0
            elif button_clicked==1 and Button1.value():      # release 1
                time_released=time.ticks_ms()
            elif button_clicked==2 and Button2.value():      # release 2
                time_released=time.ticks_ms()
            
            time.sleep_ms(100)
            
 
    def battery_read():

        bat=ADC(Pin(34))
        bat.atten(ADC.ATTN_11DB)    # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
        ENABLE_BAT = Pin(14, Pin.OUT)

        ENABLE_BAT.on()
        val=0
        for n in range(100):
            val+=bat.read()
        ENABLE_BAT.off()
        vb=(val/100)/4096*3.6*2
        print("BATTERY=",vb)
        return "Vbat=%.1fV" % vb



#    _thread.start_new_thread(threadFunction, ())


    class TFT():
        
        NOTHING=0
        BUTTON1_SHORT=11
        BUTTON2_SHORT=21
        BUTTON1_LONG=12
        BUTTON2_LONG=22
        BUTTON1_DCLICK=13
        BUTTON2_DCLICK=23
        
        RIGHT_BOTTOM=0
        RIGHT_TOP=1
        LEFT_BOTTOM=2
        LEFT_TOP=3

        # Color definitions
        BLACK = 0x0000
        BLUE = 0x001F
        RED = 0xF800
        GREEN = 0x07E0
        CYAN = 0x07FF
        MAGENTA = 0xF81F
        YELLOW = 0xFFE0
        WHITE = 0xFFFF
        GREY1=(50 & 0xf8) << 8 | (50 & 0xfc) << 3 | 50 >> 3
        GREY2=(150 & 0xf8) << 8 | (150 & 0xfc) << 3 | 150 >> 3
        
        
        def get_color(self,r=0, g=0, b=0):
            return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3
        
        def _encode_pixel(self,color):
                """Encode a pixel color into bytes."""
                return struct.pack(_ENCODE_PIXEL, color)

        def _encode_pos(self,x, y):
                """Encode a postion into bytes."""
                return struct.pack(_ENCODE_POS, x, y)


        @micropython.viper
        def display_write(self,command:int,data):
            #print("display_write(command,data) = ",command,data,type(data),type(None))
                
                #print(int(data[0]))
            GPIO_OUT = ptr32(gpio_base_register)      # GPIO base register  u=int(1<<31)
            GPIO_OUT[2]=PIN_CS                        # PIN_CS=Pin(5)=0     cs.value(0)
            if command != 0:
                GPIO_OUT[1]=PIN_CLK                   # PIN_CLK=Pin(18)=1   clk.value(1)
                GPIO_OUT[2]=PIN_DC                    # PIN_DC=Pin(16)=0    dc.value(0)
                self.spi.write(bytes([command]))
            if type(data) is not type(None):
                GPIO_OUT[1]=PIN_CLK                   # PIN_CLK=Pin(18)=1   clk.value(1)
                GPIO_OUT[1]=PIN_DC                    # PIN_DC=Pin(16)=1    dc.value(1)
                self.spi.write(data)
            GPIO_OUT[1]=PIN_CS                        # PIN_CS=Pin(5)=1     cs.value(1)


        def display_alloc(self,b,nb):
            return(b * nb)


        @micropython.viper
        def display_start(self):

            GPIO_OUT = ptr32(gpio_base_register)    # GPIO base register  u=int(1<<31)
            GPIO_OUT[1]=PIN_BL                             # PIN_BL=Pin(4)=1  bl.value(1)
            # hard_reset 
            GPIO_OUT[2]=PIN_CS                             # PIN_CS=Pin(5)=0   cs.value(0)
            GPIO_OUT[1]=PIN_RST                            # PIN_CS=Pin(23)=1  rst.value(1)
            time.sleep_ms(50)
            GPIO_OUT[2]=PIN_RST                            # PIN_CS=Pin(23)=0  rst.value(0)
            time.sleep_ms(50)
            GPIO_OUT[1]=PIN_RST                            # PIN_CS=Pin(23)=1  rst.value(1)
            time.sleep_ms(150)
            GPIO_OUT[1]=PIN_CS                             # PIN_CS=Pin(5)=1   cs.value(1)
            # soft_reset
            self.display_write(ST77XX_SWRESET,None)
            time.sleep_ms(150)
            #self.sleep_mode(False)
            self.display_write(ST77XX_SLPOUT,None)
            # set_color_mode()
            self.display_write(ST77XX_COLMOD,bytes([0x55]))
            # set_mem_access_mode()
            self.display_write(ST7789_MADCTL,bytes([16]))
            # inversor_mode(True)
            self.display_write(ST77XX_INVON,None)
            self.display_write(ST77XX_NORON,None)
            #print(self._encode_pos(0+DISPLAY_XSTART,134+DISPLAY_XSTART))
            self.display_write(ST77XX_CASET,self._encode_pos(0+DISPLAY_XSTART,134+DISPLAY_XSTART))
            #print(self._encode_pos(0+DISPLAY_XSTART,134+DISPLAY_XSTART))
            self.display_write(ST77XX_RASET,self._encode_pos(0+DISPLAY_YSTART,239+DISPLAY_YSTART))
            #print(self._encode_pos(0+DISPLAY_YSTART,239+DISPLAY_YSTART))

            self.display_write(ST77XX_RAMWR,None)

            GPIO_OUT[1]=PIN_DC                    # PIN_DC=Pin(16)=1    dc.value(1)
            self.display_write(ST77XX_DISPON,None)
                    
            
            """
            ########################### CLEAR DISPLAY
            chunks, rest = divmod(DISPLAY_WIDTH * DISPLAY_HEIGHT, _BUFFER_SIZE)
            #print("chunks, rest=",chunks,rest)
            pixel = self._encode_pixel(self.BLACK)
            #dc.value(1)
            GPIO_OUT[1]=PIN_DC                    # PIN_DC=Pin(16)=1    dc.value(1)
            #data=self.display_alloc(pixel,_BUFFER_SIZE)
            #data_mview=memoryview(data)
            
            if chunks:
                data=self.display_alloc(pixel,_BUFFER_SIZE)
                for _ in range(126):
                    self.display_write(0, data)
                #del data
            if rest:
                data=self.display_alloc(pixel,rest)
                self.display_write(0, data)
                #self.display_write(0, data[0:rest])
            #del data
            self.display_write(ST77XX_DISPON,None)
            """
     

        def __init__(self,code=''):
                       
            self.wifi_status=False
            self.wifi_logo_x0=-1
            self.wifi_logo_y0=-1
            
            self.work_flag=True
            
            self.width = 135
            self.height = 240

            self.bl = machine.Pin(4, machine.Pin.OUT)
            self.cs = machine.Pin(5, machine.Pin.OUT)
            self.reset = machine.Pin(23, machine.Pin.OUT)
            self.dc = machine.Pin(16, machine.Pin.OUT)
            
            self.spi = machine.SPI(
                1,
                baudrate=20000000,
                polarity=1,
                phase=1,
                sck=machine.Pin(18),
                mosi=machine.Pin(19))

            self.display_start()
            self.display_set()

            self.Arial16=Font('arial_16')

            print("Class TFT: __init__()")
            self.display_set(self.WHITE)

            vb=battery_read()
            
            self.modulo_id=unique_id()
            if len(self.modulo_id)==6:
                self.display_write_str(self.Arial16,"%02X%02X %02X%02X %02X%02X"%
                                       (self.modulo_id[0],self.modulo_id[1],
                                        self.modulo_id[2],self.modulo_id[3],
                                        self.modulo_id[4],self.modulo_id[5]),
                                       10,10,self.BLACK,self.WHITE)
            self.display_write_str(self.Arial16,vb,155,10,self.BLUE,self.WHITE)

            self.display_load_image("TecnicoLisboa_2",60,35)
            
            if len(self.modulo_id)==6:
                self.display_write_str(self.Arial16,"%02X%02X %02X%02X %02X%02X"%
                                       (self.modulo_id[0],self.modulo_id[1],
                                        self.modulo_id[2],self.modulo_id[3],
                                        self.modulo_id[4],self.modulo_id[5]),
                                       10,10,self.BLACK,self.WHITE)
            self.display_write_str(self.Arial16,vb,155,10,self.BLUE,self.WHITE)
            
            time.sleep_ms(DELAY_START_MS)
            self.display_set(self.BLACK)
                        
            self.wifi=wifiClass("SSID","PASSWORD")      # Corrigir
            self.wifi_status=self.wifi.wifi_start(TIMEOUT_WIFI_START)
            #self.set_wifi_logo()
            _thread.start_new_thread(threadFunction, (self,))

            
                        
        def set_wifi_icon(self,x0,y0):
            if self.wifi_logo_x0==-1:
               self.display_load_image("WIFI_GREY", x0, HEIGHT-y0-16)
            self.wifi_logo_x0=x0
            self.wifi_logo_y0=y0
            if self.wifi_status:
                self.display_load_image("WIFI_ON", x0, HEIGHT-y0-16)
            else:
                self.display_load_image("WIFI_OFF", x0, HEIGHT-y0-16)


        def send_mail(self,delta_t, pontos_v, corpo,address):
            self.display_load_image("WIFI_GREY", self.wifi_logo_x0, HEIGHT-self.wifi_logo_y0-16)
            url = "http://raposa.ist.utl.pt/se/SendMail.php"
            csv=""
            for n in range(len(pontos_v)):
                csv += "%.4f,%.3f\n" % (delta_t * n, pontos_v[n])  # Pontos com 6 casas decimais

            headers = {'Content-Type': 'application/x-www-form-urlencoded'}

            data = 'address=%s&subject=Points from uOscilloscope&body=Points from uOscilloscope: %d points\n\n%s&attachment=%s' % (address,len(pontos_v),corpo,csv)
            #print("data=",data)
            try:
#                result = requests.post(url,data="address=pvitor@ist&subject=sss sss",headers=headers)
                result = requests.post(url,data=data,headers=headers)
            except Exception as e:
                print("send_mail(): Failed (ERROR 1)",e)
                self.display_load_image("WIFI_OFF", self.wifi_logo_x0, HEIGHT-self.wifi_logo_y0-16)
                return

            #print(result.text)
            if "Points from uOscilloscope:" in result.text:
                print("send_mail(): OK")
                self.display_load_image("WIFI_ON", self.wifi_logo_x0, HEIGHT-self.wifi_logo_y0-16)
            else:
                print("send_mail(): Failed (ERROR 2)")
                self.display_load_image("WIFI_OFF", self.wifi_logo_x0, HEIGHT-self.wifi_logo_y0-16)
            #print(result.text)
            del csv
            del headers
            del url
            del data


        def _set_color_mode(self, mode):
            self.write(ST77XX_COLMOD, bytes([mode & 0x77]))


        #def display_set(self,color=BLACK,x=0,y=0,w=DISPLAY_WIDTH,h=DISPLAY_HEIGHT):
        def display_set(self,color=BLACK,y=0,x=0,h=DISPLAY_HEIGHT,w=DISPLAY_WIDTH):
            #x=135-x-w
            
            #x=DISPLAY_WIDTH-x
        #     print("---",x,y,w,h)
            self.display_write(ST77XX_CASET,self._encode_pos(x+DISPLAY_XSTART,x+w-1+DISPLAY_XSTART))
        #     print(x+DISPLAY_XSTART,x+w-1+DISPLAY_XSTART)
        #     print(_encode_pos(x+DISPLAY_XSTART,x+w-1+DISPLAY_XSTART))
            self.display_write(ST77XX_RASET,self._encode_pos(y+DISPLAY_YSTART,y+h-1+DISPLAY_YSTART))
        #     print(y+DISPLAY_YSTART,y+h-1+DISPLAY_YSTART)
        #     print(_encode_pos(y+DISPLAY_YSTART,y+h-1+DISPLAY_YSTART))

            self.display_write(ST77XX_RAMWR,None)

           # chunks, rest = divmod(DISPLAY_SQUARE, _BUFFER_SIZE)
            chunks, rest = divmod(w*h, _BUFFER_SIZE)
            ch=int(chunks)
            pixel = self._encode_pixel(color)
            self.dc.value(1)
            if ch:
                data=self.display_alloc(pixel,_BUFFER_SIZE)
                for _ in range(ch):
                    self.display_write(0, data)
            if rest:
                data=self.display_alloc(pixel,rest)
                self.display_write(0, data)

        
        def display_pixel(self,color=BLACK,y=0,x=0):
            #x=134-x            # x=135-x-w    (w=1)
            self.display_write(ST77XX_CASET,self._encode_pos(x+DISPLAY_XSTART,x+DISPLAY_XSTART))
            self.display_write(ST77XX_RASET,self._encode_pos(y+DISPLAY_YSTART,y+DISPLAY_YSTART))
            self.display_write(ST77XX_RAMWR,None)
            pixel = self._encode_pixel(color)
            self.dc.value(1)
            self.display_write(0, pixel)


        def display_npixel(self,color,y,x):
            
            pixel = self._encode_pixel(color)
            for n in range(len(y)):
#                self.display_write(ST77XX_CASET,self._encode_pos(134-x[n]+DISPLAY_XSTART,134-x[n]+DISPLAY_XSTART))
                self.display_write(ST77XX_CASET,self._encode_pos(x[n]+DISPLAY_XSTART,x[n]+DISPLAY_XSTART))
                self.display_write(ST77XX_RASET,self._encode_pos(y[n]+DISPLAY_YSTART,y[n]+DISPLAY_YSTART))
                self.display_write(ST77XX_RAMWR,None)
                self.display_write(0, pixel)

        def display_line(self,color,y_0,x_0,y_1,x_1):
            
            pixel = self._encode_pixel(color)
            
            d_x = abs(x_1 - x_0)
            d_y = abs(y_1 - y_0)
            x, y = x_0, y_0
            s_x = -1 if x_0 > x_1 else 1
            s_y = -1 if y_0 > y_1 else 1
            if d_x > d_y:
                err = d_x / 2.0
                while x != x_1:
                    #self.pixel(x, y, color)
                    self.display_write(ST77XX_CASET,self._encode_pos(x+DISPLAY_XSTART,x+DISPLAY_XSTART))
                    self.display_write(ST77XX_RASET,self._encode_pos(y+DISPLAY_YSTART,y+DISPLAY_YSTART))
                    self.display_write(ST77XX_RAMWR,None)
                    self.display_write(0, pixel)
                    err -= d_y
                    if err < 0:
                        y += s_y
                        err += d_x
                    x += s_x
            else:
                err = d_y / 2.0
                while y != y_1:
                    #self.pixel(x, y, color)
                    self.display_write(ST77XX_CASET,self._encode_pos(x+DISPLAY_XSTART,x+DISPLAY_XSTART))
                    self.display_write(ST77XX_RASET,self._encode_pos(y+DISPLAY_YSTART,y+DISPLAY_YSTART))
                    self.display_write(ST77XX_RAMWR,None)
                    self.display_write(0, pixel)
                    err -= d_x
                    if err < 0:
                        x += s_x
                        err += d_y
                    y += s_y
            #self.pixel(x, y, color)
            self.display_write(ST77XX_CASET,self._encode_pos(x+DISPLAY_XSTART,x+DISPLAY_XSTART))
            self.display_write(ST77XX_RASET,self._encode_pos(y+DISPLAY_YSTART,y+DISPLAY_YSTART))
            self.display_write(ST77XX_RAMWR,None)
            self.display_write(0, pixel)
            
            
        def display_nline(self,color,y,x):
            
            for n in range(len(x)-1):
                self.display_line(color,y[n],x[n],y[n+1],x[n+1])


        def display_load_image(self,name,y=0,x=0):

            t1=time.ticks_us()
            filename_bmp='Images/'+name+'.bmp'
            filename_bin='Images/'+name+'.bin'

            #print("################",filename_bmp,file_exists(filename_bmp))
            #print("################",filename_bin,file_exists(filename_bin))

            #print("gc.mem_free()=",gc.mem_free())
            
            if not file_exists(filename_bin):
                if not file_exists(filename_bmp):
                    print("ERROR: display_load_image() - File %s does not exist"%filename_bmp)
                    return
                
                gc.collect()
                img=prvReadBMP(filename_bmp)
                pix=bytearray('')
                for py in range(img.height):
                    for px in range(img.width):
                        r,g,b = img._read_pixel(px,img.height-py-1)
                        cor=img.color565(b,g,r)                    
                        pix+=cor.to_bytes(2,'big')
                    #print(len(pix),gc.mem_free())
                    gc.collect()
                        #print(gc.mem_free())
                file = open(filename_bin, "wb")
                file.write(img.width.to_bytes(2, 'little'))
                file.write(img.height.to_bytes(2, 'little'))
                file.write(pix)
                file.close()
                gc.collect()
                print("TFT.display_load_image(): File %s created"%filename_bin)
                del pix
                del img
                
                
                
                
            #print("..................................................",__file__)
            #print("################",filename_bmp,file_exists(filename_bmp))
            #print("################",filename_bin,file_exists(filename_bin))
            
            """
            file = open(filename_bin,"rb")
            pointer=0
            pix=bytearray(10000)
            ch=b''
            while(1):
                ch=file.read(1)
                if ch==b'':
                    break
                pix[pointer]=ord(ch)
                pointer += 1
                gc.collect()
            file.close()
            print("...................................         ",pointer)
            
            #pix = file.read()
            #pix_mview=memoryview(pix)
            #file.close()
            del file
            del pix
            del pointer
            gc.collect()
            #del pix_mview
            return
            
            
            #file = open(filename_bin,"rb")
            #pix = file.read()
            #pix_mview=memoryview(pix)
            """
            
            #pix=bytearray(10000)
            file = open(filename_bin,"rb")
            
            
            b0=ord(file.read(1))
            b1=ord(file.read(1))
            b2=ord(file.read(1))
            b3=ord(file.read(1))

            
            w=b0+b1*256
            h=b2+b3*256
            nbytes=w*h*2
            pix=bytearray(nbytes)

            x=DISPLAY_WIDTH-w-x
            
            del b0
            del b1
            del b2
            del b3

            ch=b''
            nbytes=0
            while(1):
                ch=file.read(1)
                if ch==b'':
                    break
                pix[nbytes]=ord(ch)
                nbytes+=1
                if nbytes%100==0:
                    gc.collect()
                del ch
            file.close()
            del file
            
        
            self.display_write(ST77XX_CASET,self._encode_pos(x+DISPLAY_XSTART,x+w-1+DISPLAY_XSTART))
            self.display_write(ST77XX_RASET,self._encode_pos(y+DISPLAY_YSTART,y+h-1+DISPLAY_YSTART))
            self.display_write(ST77XX_RAMWR,None)
            self.display_write(0, pix)
            del pix
            gc.collect()

            return
            
            #w=int.from_bytes(pix_mview[0:2],'little')
            #h=int.from_bytes(pix_mview[2:4],'little')
            w=pix_mview[0]+pix_mview[1]*256
            h=pix_mview[2]+pix_mview[3]*256
            #print('display_load_image:',w,h,pix_mview[0:2],pix_mview[2:4])
            
            #del pix
            #del pix_mview
            gc.collect()
            
            
        #     print("---",x,y,w,h)
            self.display_write(ST77XX_CASET,self._encode_pos(x+DISPLAY_XSTART,x+w-1+DISPLAY_XSTART))
        #     print(x+DISPLAY_XSTART,x+w-1+DISPLAY_XSTART)
        #     print(_encode_pos(x+DISPLAY_XSTART,x+w-1+DISPLAY_XSTART))
            self.display_write(ST77XX_RASET,self._encode_pos(y+DISPLAY_YSTART,y+h-1+DISPLAY_YSTART))
        #     print(y+DISPLAY_YSTART,y+h-1+DISPLAY_YSTART)
        #     print(_encode_pos(y+DISPLAY_YSTART,y+h-1+DISPLAY_YSTART))

            self.display_write(ST77XX_RAMWR,None)

            chunks, rest = divmod(w*h, _BUFFER_SIZE)
            #print(type(chunks),chunks)
            ch=int(chunks)
            #print(type(ch),ch)
            #pixel = _encode_pixel(color)
            self.dc.value(1)
            ptr=4
            #print("----------------->",len(pix),chunks,rest)
            
                    
            if ch:
                #data=display_alloc(pixel,_BUFFER_SIZE)
                for _ in range(ch):
                    self.display_write(0, pix_mview[ptr:ptr+_BUFFER_SIZE*2])
                    #print(_,len(image[ptr:ptr+_BUFFER_SIZE*2]))
                    ptr+=_BUFFER_SIZE*2
            if rest:
                #data=display_alloc(pixel,rest)
                self.display_write(0, pix_mview[ptr:ptr+rest*2])
            #print(len(image[ptr:ptr+rest*2]))

            print("TFT.display_load_image(\'%s\'): %f s" % (name,(time.ticks_us()-t1)/1000000)) 
            del pix
            del pix_mview
            del t1
            del chunks
            del rest
            del ch
            del ptr
            del w
            del h
            del filename_bmp
            del filename_bin
            gc.collect()
            

        def display_write_grid(self,x=0,y=0,w=WIDTH,h=HEIGHT,nx=10,ny=8,center_lines=True,line_color=GREY1,border_color=GREY2):
            if nx%2 !=0 or ny%2 !=0:
                return
            dx=(w-1)/nx
            dy=(h-1)/ny
            for n in range(nx+1):
                if n==0 or n==nx:
                    self.display_set(border_color, int(x+dx*n+0.5), y, 1, h-1)
                elif n==nx/2:
                    if center_lines:
                        self.display_set(border_color, int(x + dx * n + 0.5), y, 1, h - 1)
                    else:
                        self.display_set(line_color, int(x + dx * n + 0.5), y, 1, h - 1)
                else:
                    self.display_set(line_color, int(x+dx*n+0.5), y, 1, h-1)
            for n in range(ny+1):
                if n==0 or n==ny:
                    self.display_set(border_color, x, int(y+dy*n+0.5), w-1, 1)
                elif n==ny/2:
                    if center_lines:
                        self.display_set(border_color, x, int(y + dy * n + 0.5), w - 1, 1)
                    else:
                        self.display_set(line_color, x, int(y + dy * n + 0.5), w - 1, 1)
                else:
                    self.display_set(line_color, x, int(y+dy*n+0.5), w-1, 1)


        def display_write_ch(self,ft,ch,y=0,x=0,foreground=0xffff,background=0x0000):
            
            image,w,h=ft.get_image(ch,foreground,background)
            image_mview=memoryview(image)
            #y-=h
            self.display_write(ST77XX_CASET,self._encode_pos(x+DISPLAY_XSTART,x+w-1+DISPLAY_XSTART))
            self.display_write(ST77XX_RASET,self._encode_pos(y+DISPLAY_YSTART,y+h-1+DISPLAY_YSTART))

            self.display_write(ST77XX_RAMWR,None)

            chunks, rest = divmod(w*h, _BUFFER_SIZE)
            ch=int(chunks)
            self.dc.value(1)
            ptr=0
            if ch:
                for _ in range(ch):
                    self.display_write(0, image_mview[ptr:ptr+_BUFFER_SIZE*2])
                    ptr+=_BUFFER_SIZE*2
            if rest:
                self.display_write(0, image_mview[ptr:ptr+rest*2])
                
            del image,w,image_mview

            return(h)


        # Aprox. 60ms para Arial_50  e 15ms para Arial_20
        def display_write_str(self,ft,str1,y=0,x=0,foreground=0xffff,background=0x0000):
     
            htot=0
            for ch in str1:
                h=self.display_write_ch(ft,ch,y,x,foreground,background)
                y+=h
                htot+=h
                
                
                
                """
                #t1=time.ticks_us()
                image,w,h=ft.get_image(ch,foreground,background)
                #print("(w,h,ch)=",w,h,ch,ord(ch))        # for debug
                image_mview=memoryview(image)
                #y-=h
                htot+=h
                self.display_write(ST77XX_CASET,self._encode_pos(x+DISPLAY_XSTART,x+w-1+DISPLAY_XSTART))
                self.display_write(ST77XX_RASET,self._encode_pos(y+DISPLAY_YSTART,y+h-1+DISPLAY_YSTART))

                self.display_write(ST77XX_RAMWR,None)

                chunks, rest = divmod(w*h, _BUFFER_SIZE)
                ch1=int(chunks)
                self.dc.value(1)
                ptr=0
                if ch1:
                    for _ in range(ch1):
                        self.display_write(0, image_mview[ptr:ptr+_BUFFER_SIZE*2])
                        ptr+=_BUFFER_SIZE*2
                if rest:
                    self.display_write(0, image_mview[ptr:ptr+rest*2])
                    
                #t2=time.ticks_us()
                #print("display_write_ch() ",ch,"   time=",t2-t1)
                #del t1,t2
                """
            return(htot)


        def readButton(self):
            global button_clicked
            global time_clicked
            global time_released

            time.sleep_ms(10)
            if button_clicked!=0 and time_released!=0:
                dt=time.ticks_diff(time_released,time_clicked)
                bt=button_clicked
                button_clicked=0
                if dt<500:
                    for n in range(25):     # 250ms
                        if button_clicked==bt:
                            while time_released==0:
                                time.sleep_ms(10)
                            button_clicked=0
                            time_clicked=0
                            time_released=0
                            if bt==1:
                                return self.BUTTON1_DCLICK
                            elif bt==2:
                                return self.BUTTON2_DCLICK
                        time.sleep_ms(10)
                if bt==1:
                    if dt<=500:
                        return self.BUTTON1_SHORT
                    else:
                        return self.BUTTON1_LONG
                elif bt==2:
                    if dt <= 500:
                        return self.BUTTON2_SHORT
                    else:
                        return self.BUTTON2_LONG
            return self.NOTHING


        def working(self):
            return self.work_flag


        def read_adc(self,npoints,total_interval):
            interval=int(total_interval*1000/npoints+0.5)
            if interval<160 or npoints>240 or (total_interval!=50 and total_interval!=100 and total_interval!=200 and total_interval!=500):
                for n in range(npoints):
                    memoria_adc[n]=0
                return memoria_adc
            t1=time.ticks_us()
            deadline=time.ticks_add(t1,interval)      # 155us mínimo leitura com deadline, 91us sem deadline
            for n in range(npoints):
                while time.ticks_diff(deadline,time.ticks_us())>0:
                    pass
                memoria_adc[n]=adc1.read()
                deadline=time.ticks_add(deadline,interval)  
                                   
            return memoria_adc
            
            
            
        """
        class TFT():
            NOTHING=0
            BUTTON1_SHORT=1
            BUTTON2_SHORT=2
            BUTTON1_LONG=3
            BUTTON2_LONG=4
    
            BLACK = 0x0000
            BLUE = 0x001F
            RED = 0xF800
            GREEN = 0x07E0
            CYAN = 0x07FF
            MAGENTA = 0xF81F
            YELLOW = 0xFFE0
            WHITE = 0xFFFF
            win=None
        
        
            def __init__(self, *args, **kwargs):
                pass
        
        
            def display_set(self, color=BLACK, x=0, y=0, w=DISPLAY_WIDTH, h=DISPLAY_HEIGHT):
                print("display_set()",color,x,y,w,h)
                #self.win.signal_message.emit(('DISPLAY_SET',color,x,y,w,h))
        """

    ##############################  WIFI  ################################
        
    try:
      import usocket as socket
    except:
      import socket
    #from machine import Pin
    import network
    import esp
    import gc
    import os
    import time
    import machine

    MAX_FAIL_LOAD_SETUP=13      # 23 segundos cada falha (5 minutos ==> MAX_FAIL_SETUP=13         (DEBUG=3)
    TIMEOUT_WIFI_START = 10    # valor em segundos (5 minutos ==> TIMEOUT_WIFI_START=600         (DEBUG=120)
    MAX_FAIL_CONNECTIONS = 16   # 18.5 segundos cada falha (5 minutos ==> MAX_FAIL_CONNECTIONS=16 (DEBUG=3)



    class wifiClass():

        def __init__(self,ssid,password):
          
            print("wifiClass(): __init__")
            self.ssid=ssid
            self.password=password
            esp.osdebug(None)
            gc.collect()

            self.interface = network.WLAN(network.STA_IF)
            #print(self.interface.isconnected())
          

        # ############################## wifi_active() ################################
        def wifi_active(self):
          return(self.interface.active())
          
          

        # ############################## wifi_start() ################################
        def wifi_start(self,timeout):
          
          #self.interface.active(False)
          if self.interface.active() and self.interface.isconnected():
              #print('wifiStart: Already connected')
              #print('wifiStart: \tConnection successful (ssid=%s, t=%ds)' % (net['SSID'],(t*200+500)/1000))
              #print('wifiStart: \t',self.interface.ifconfig())
              self.mac_address=''.join('{:02x}'.format(x) for x in self.interface.config('mac'))
              #print('wifiStart: \t',self.mac_address)
              return(True)

          if self.ssid=="SSID":
              return False
            

          self.interface.active(True)
          flag=True
          while flag:
                print('wifiStart: \tTrying to connect to ssid - %s' % self.ssid)
                self.interface.connect(self.ssid,self.password)
                for t in range(0, timeout*5):            # Cada passagem são 0.2 segundos timeout/0.2=timeout*5
                  if self.interface.isconnected():
                    flag=False
                    break
                  if t%25==0: print("waiting... ("+str(t*0.2)+")")
                  time.sleep_ms(200)
                if self.interface.isconnected():
                  break
                else:
                    #print("failed to connect and going to reset ...")
                    #machine.reset()
                    print("wifiStart(): Failed to connect")
                    return(False)
                    
          print('wifiStart: \tConnection successful (ssid=%s, t=%ds)' % (self.ssid,(t*200+500)/1000))
          #print('wifiStart: \t',self.interface.ifconfig())
          #self.interface.ifconfig(('192.168.200.201', '255.255.255.0', '192.168.200.254', '8.8.8.8'))
          #print('wifiStart: \t',self.interface.ifconfig())
    #      self.mac_address=''.join('{:02x}'.format(x) for x in self.interface.config('mac'))
    #      print('wifiStart (mac):\t',self.mac_address)
          #time.sleep_ms(200)
          return(True)
          
        def set_ip(self,ip_number):
            ifc=self.interface.ifconfig()
            print((ifc[0],ifc[1],ifc[2],str(ip_number)))
            self.interface.ifconfig((str(ip_number),ifc[1],ifc[2],ifc[3]))
            print('set_ip: \t',self.interface.ifconfig())
          



else:
    MICROPYTHON = False
    import T_Simulator
    from T_Simulator import TFT


def Convert565(color):
    return ((color >> 11) & 0b011111)<<3, ((color >> 5) & 0b0111111)<<2, (color & 0b011111) << 3

class Font:
    def __init__(self, name):
        self.dictFont = {}
        tmp = name.split('_')
        self.name = tmp[0]
        if len(tmp) == 2:
            self.npix = tmp[1]
        else:
            self.npix = 1
        del tmp
        print(".........................", "prvDisplay.fonts.", self.name, self.npix)
#        ft = __import__("prvDisplay.fonts." + name, globals(), locals(), ['_font'], 0)
        ft = __import__( name, globals(), locals(), ['_font'], 0)
        print(".........................", "prvDisplay.fonts.", self.name, self.npix, len(ft._font))
        self.font = ft
        # print("Font: Font name [%s] imported" % self.name)

    def get_pix(self, ch):
        # (p,w,h)=self.font.get_ch(ch)
        # print(w,h,''.join('{:02x}'.format(x) for x in bytes(p)))
        return (self.font.get_ch(ch))

    def get_image(self, ch, foreground, background):

        #       if (ch.isdigit() or ch=='.') and ch in self.dictFont:
        #           #print(">>>>>>>>>>>>>",ch,"EXISTE")
        #           return(self.dictFont[ch][0],self.dictFont[ch][1],self.dictFont[ch][2])
        #       else:
        # print(">>>>>>>>>>>>>",ch,"NÃO EXISTE",len(self.dictFont))
        (pix, width, height) = self.font.get_ch(ch)
        # print(width,height,foreground,background,''.join('{:02x}'.format(x) for x in bytes(pix)))

        foreground_bytes = foreground.to_bytes(2, 'big')
        background_bytes = background.to_bytes(2, 'big')

        count = width * height * 2
        # print("get_image(): alocating: %d bytes"%count,width,height,ch)
        image = bytearray(count)
        img_ptr = 0
        pix_ptr = 0
        bit = 0
        for y in range(height):
            # print()
            if bit != 0:
                bit = 0
                pix_ptr += 1
            for x in range(width):
                # print("x=%d y=%d img_ptr=%d pix_ptr=%d bit=%d"%(x,y,img_ptr,pix_ptr,bit))
                #                if img_ptr<count:
                # ptr=img_ptr+2*width*(height-1)-y*4*width
                ptr = -2 * x + (y + 1) * (width) * 2 - 2
                #                         print("ptr=",ptr)
                if (0x01 << bit) & pix[pix_ptr]:
                    image[ptr] = foreground_bytes[0]
                    image[ptr + 1] = foreground_bytes[1]
                    # print('#',end='')
                else:
                    image[ptr] = background_bytes[0]
                    image[ptr + 1] = background_bytes[1]
                    # print(" ",end='')
                img_ptr += 2
                bit += 1
                if bit >= 8:
                    bit = 0
                    pix_ptr += 1

        #            self.dictFont[ch]=[image,width,height]

        return (image, width, height)


