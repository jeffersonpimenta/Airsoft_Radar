#!/usr/bin/python
#coding: utf-8

import os#lib do fopen
import subprocess
import time
import signal
from espeak import espeak
import  RPi.GPIO as GPIO

espeak.set_voice('brazil')
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN,pull_up_down=GPIO.PUD_UP)

#f1=429000000
#f2=431000000
f1=136000000
f2=174000000
f3=400000000
f4=520000000
p=2500
th=10.0
maior=th

while 1:
    ff1=0
    ff2=0
    pp=0
    k=0
    comando = 'rtl_power -f '+str(f1)+':'+str(f2)+':'+str(p)+' -g 9 -i 1 -1'#monta comando
    saida=os.popen(comando).readlines()#executa o comando
    
    while k<len(saida):
        linha=saida[k].split(",")#pega primeira linha
        k+=1
        ff1=int(linha[2])#pega freq inicial
        ff2=int(linha[3])#pega freq final
        pp=float(linha[4])#pega passo

        i=6#inicio dos valores de frequencia
        while i<len(linha):
            if float(linha[i])>maior:
                maior=float(linha[i])#pega maior valor de th
                
            if float(linha[i])>=th:
                print("{:,.0f}".format((ff1+((i-6)*pp)+270000)/1000),' - ',str(linha[i]),'dB')
                espeak.synth('frequencia '+"{:,.0f}".format((ff1+((i-6)*pp)+270000)/1000))
                time.sleep(3)
                comando = 'rtl_fm -f '+str(ff1+((i-6)*pp))+' -s 44100 -g 9 -l 0 - | aplay -t raw -f S16_LE -r 44100 -c 1' #monta comando
                #print(comando)
                proc1 = subprocess.Popen(comando,shell=True)
                while GPIO.input(19):
                    time.sleep(0.1)
                subprocess.call(['killall', 'rtl_fm'])
                proc1.wait()
            i+=1
    
    ff1=0
    ff2=0
    pp=0
    k=0
    comando = 'rtl_power -f '+str(f3)+':'+str(f4)+':'+str(p)+' -g 9 -i 1 -1'#monta comando
    saida=os.popen(comando).readlines()#executa o comando
    
    while k<len(saida):
        linha=saida[k].split(",")#pega primeira linha
        k+=1
        ff1=int(linha[2])#pega freq inicial
        ff2=int(linha[3])#pega freq final
        pp=float(linha[4])#pega passo

        i=6#inicio dos valores de frequencia
        while i<len(linha):
            if float(linha[i])>maior:
                maior=float(linha[i])#pega maior valor de th
                
            if float(linha[i])>=th:
                print("{:,.0f}".format((ff1+((i-6)*pp)+270000)/1000),' - ',str(linha[i]),'dB')
                espeak.synth('frequencia '+"{:,.0f}".format((ff1+((i-6)*pp)+270000)/1000))
                time.sleep(3)
                comando = 'rtl_fm -f '+str(ff1+((i-6)*pp))+' -s 44100 -g 9 -l 0 - | aplay -t raw -f S16_LE -r 44100 -c 1' #monta comando
                #print(comando)
                proc1 = subprocess.Popen(comando,shell=True)
                while GPIO.input(19):
                    time.sleep(0.1)
                subprocess.call(['killall', 'rtl_fm'])
                proc1.wait()
            i+=1
            
    if GPIO.input(26) == False:
        th=th-1
        espeak.synth('ganho de ' + str(th))
    if GPIO.input(13) == False:
        th=th+1
        espeak.synth('ganho de ' + str(th))