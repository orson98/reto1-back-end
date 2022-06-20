import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from tkinter import  *
from tkinter.ttk import Treeview

app = Tk()
app.geometry('300x100')
app.title('reto1')

url = requests.get("https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioPromedio.aspx")


def grabarMonedas(monedas):
    
    strMonedas = ""
    for l in monedas:
        for clave,valor in l.items():
            strMonedas += valor
            if clave != 'venta':
                strMonedas += ';'
            else:
                strMonedas += '\n'
    return strMonedas



class Cambio:

    def __init__(self,window):
        self.wind = window
        self.wind.title('cambio sbs')
        self.wind.geometry('700x600')
        self.wind.configure(bg='#49A')
        
    self.TrvAlumnos = Treeview(height=10,columns=2)
        self.TrvAlumnos.grid(row=5,column=0,columnspan=2,padx=10)
        self.TrvAlumnos.heading('#0',text='Moneda',anchor=CENTER)
        self.TrvAlumnos.heading('#1',text='compra',anchor=CENTER)
        self.TrvAlumnos.heading('#1',text='venta',anchor=CENTER)

        btnExportar = Button(self.wind,text='Exportar',command=self.Exportar)
        btnExportar.grid(row=2,column=0)

 

def scrapping_tipocambio():
    if(url.status_code == 200):
        print("pagina encontrada")
      
        html = BeautifulSoup(url.text,'html.parser')
        tabla = html.find_all('table',{'id':'ctl00_cphContent_rgTipoCambio_ctl00'})
    
        listaMonedas = []
        for i in range(7):
            fila = html.find('tr',{'id':'ctl00_cphContent_rgTipoCambio_ctl00__'+str(i)}) 
            moneda = fila.find('td',{'class':'APLI_fila3'})
            compra = fila.find('td',{'class':'APLI_fila2'})
            venta = fila.find('td',{'class':'APLI_fila2'}).findNext('td')
            dicMoneda = {
                'moneda': moneda.get_text(),
                'compra': compra.get_text(),
                'venta': venta.get_text()
            }
            listaMonedas.append(dicMoneda)
        
        columnas = ["moneda","compra","venta"]
        tablaMonedas = [moneda.values() for moneda in listaMonedas]
        print(tabulate(tablaMonedas,headers=columnas,tablefmt="grid"))
        strMonedas = grabarMonedas(listaMonedas)
        fw = open('monedas.csv','w')
        fw.write(strMonedas)
        fw.close()
    else:
        print("error " + str(url.status_code))

if __name__ == "__main__" :
    scrapping_tipocambio()

window = Tk()
app = Alumno(window)
window.mainloop()
