import requests
import json
from Teams import Teams
from matches import Matches
from Stadiums import Stadiums
from Clients import Clients
from Restaurants import Restaurants, Products

def equipos():
    lista_equipos = []
    url = 'https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/teams.json'
    equipos_response = requests.get(url)
    equipos_content = equipos_response.content
    equipos_json = json.loads(equipos_content.decode())
    for i in equipos_json:
        equipo = Teams(i['name'], i['flag'], i['fifa_code'], i['group'], i['id'])
        lista_equipos.append(equipo)
    return lista_equipos

def estadios():
    lista_estadios=[]
    url = 'https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/stadiums.json'
    estadios_response = requests.get(url)
    estadios_content = estadios_response.content
    estadios_json = json.loads(estadios_content.decode())
    for i in estadios_json:
        estadio = Stadiums(i['id'], i['name'], i['capacity'], i['location'], i['restaurants'])
        lista_estadios.append(estadio)
    return lista_estadios

def partidos(lista_equipos, lista_estadios):
    lista_partidos=[]
    url = 'https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/matches.json'
    partidos_response = requests.get(url)
    partidos_content = partidos_response.content
    partidos_json = json.loads(partidos_content.decode())
    for i in partidos_json:
        for j in lista_estadios:
            if i['stadium_id'] == j.id:
                estadio = j.name
                sillas_generales = j.capacity[0]
                sillas_vip = j.capacity[1]
                vip, generales = create_matrix(sillas_generales, sillas_vip)
        for x in lista_equipos:
            if i['home_team'] == x.name:
                local = x.name
            if i['away_team'] == x.name:
                visitante = x.name
        entradas_validadas = sillas_disponibles(sillas_generales, sillas_vip)
        partido = Matches(local, visitante, i['date'].split(' ')[0], i['date'].split(' ')[1], estadio, i['id'], generales, vip, entradas_validadas)
        lista_partidos.append(partido)
    return lista_partidos

def create_matrix(sillas_generales, sillas_vip):
    #Esta funcion crea dos matrices, los asientos generales y los vip
    sillas = sillas_vip
    vip = []
    fila = sillas//10
    columna = ['A','B','C','D','E','F','G','H','I','J']
    aux2=1 
    for i in range(fila):
        row = []
        aux=0
        for i in range(len(columna)):
            num = columna[aux]+str(aux2)
            aux+=1
            row.append(num)
        aux2 += 1
        vip.append(row)
    generales = []
    sillas = sillas_generales
    fila = sillas//10
    for i in range(fila):
        row = []
        aux=0
        for i in range(len(columna)):
            num = columna[aux]+str(aux2)
            aux+=1
            row.append(num)
        aux2 += 1
        generales.append(row)
    return vip, generales

def sillas_disponibles(sillas_generales, sillas_vip):
    #Esta funcion crea una matriz que seran las entradas que ya se validaron
    sillas = sillas_generales+sillas_vip
    sillas_ocupadas = []
    fila = sillas//10
    columna = ['A','B','C','D','E','F','G','H','I','J']
    aux2=1 
    for i in range(fila):
        row = []
        aux=0
        for i in range(len(columna)):
            num = columna[aux]+str(aux2)
            aux+=1
            row.append(num)
        aux2 += 1
        sillas_ocupadas.append(row)
    return sillas_ocupadas

def buscar_partidos(lista_partidos, lista_estadios, lista_equipos):
    #Funcion para buscar los partidos
    while True:
        menu = input('Please enter a valid option: \n1 Search by specific country\n2 Search by specific stadium\n3 Search by date\n4 Exit\n')
        while not menu.isnumeric() or int(menu) not in range(1,5):
            menu = input('Invalid option, try again: ')
    #Segun paises
        if menu == '1':
            pais = input('Write the country you are looking for: ').capitalize()
            aux = 0
            while True:
                for i in lista_equipos:
                    if i.name == pais:
                        aux+=1
                if aux == 0:
                    pais = input('Invalid country try again: ')
                else: 
                    break
            
            for i in lista_partidos:
                if i.local == pais or i.visitor == pais:
                    print('')
                    print(i.local,' VS. ', i.visitor, i.date, i.time,' at ', i.stadium)
            continue
    #segun estadios
        if menu == '2':
            cont = 1
            for i in lista_estadios:
                print('')
                print('Option', cont, i.name)
                cont+=1
            opt = input('Select the stadium you are looking for: ')
            while not opt.isnumeric or int(opt) not in range(len(lista_estadios)+1):
                opt = input('Invalid input, try again: ')
            for i in lista_partidos:
                if i.stadium == lista_estadios[int(opt)-1].name:
                    print('')
                    print(i.local, ' VS.', i.visitor, i.date, i.time, 'at', i.stadium)
            continue
    #Segun dia
        if menu == '3':
            month = input('Please enter the month your are looking for: \n11 November\n12 December\n')
            while not month.isnumeric() or int(month) not in range(11,13):
                month = input('Invalid input, try again')
            day = input('Enter the day you are looking for: \n (From 1-31)')
            while not day.isnumeric() or int(day) not in range(1,31):
                day = input('Invalid input, try again:')
            date = month,day,'2022'
            date = '/'.join(date)
            aux2=0
            for i in lista_partidos:
                if i.date == date:
                    print(i.local, ' VS.', i.visitor, i.date, i.time, i.stadium, i.id)  
                    print('')
                    aux2+=1
            if aux2 == '0':
                print('No games found that date')
            continue  
        else:
            break
            
def registrar_cliente(lista_partidos, clientes):
    #Funcion que toma todos los datos de los clientes, incluido el asiento
    name = input('Please enter your name: ')
    while not name.isalpha():
        name = input('Please try again: ')
    lastname = input('Please enter your lastname: ')
    while not lastname.isalpha():
        lastname = input('Please try again: ')    
    id = input('Please enter your id: ')
    while not id.isnumeric():
        id = input('Invalid id, please try again: ')
    age = input('Please enter your age: ')
    while not age.isnumeric() or int(age) not in range(1,100):
        age = input('Invalid input, please try again')
    for i in lista_partidos:
        print('Id', i.id, i.local, ' vs.', i.visitor, i.date, i.time, i.stadium)
        print('')
    partido = input('Please enter the id of the match you are looking for: ')
    aux = 0
    while True:
        for i in lista_partidos:
            if i.id == partido:
                aux+=1
        if aux == 0:
            partido = input('Invalid input, try again: ')
        else:
            break
    tipo = input('Please enter the ticket you want: \nG General 50$\nV VIP 120$\n').upper()
    while True:
        if tipo == 'G':
            tipo = 'General'
            precio = 50+50*0.16
            break
        if tipo == 'V':
            tipo = 'VIP'
            precio = 120+120*0.16
            break
        else:
            tipo = input('Invalid input, try again: ')
    lista_partidos, silla_deseada = elegir_silla(print_matrix(lista_partidos, tipo, partido), tipo, partido, lista_partidos)
    print('Your seat was reserve succesfully.')
    cliente = Clients(name, lastname, id, age, partido, tipo, silla_deseada, precio, 0)
    clientes.append(cliente)
    print('******Receipt*****')
    print('Yor seat is: ', cliente.seat)
    print('After taxes, the total amount is: ', precio)
    return lista_partidos, clientes, cliente

def print_matrix(lista_partidos, tipo, partido):
    #Funcion para imprimir los asientos
    if tipo == 'General':
        for i in lista_partidos:
            if i.id == partido:
                mat = i.sillas_generales
    if tipo == 'VIP':
        for i in lista_partidos:
            if i.id == partido:
                mat = i.sillas_vip    
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            print(mat[i][j], end='     ')
        print()
    return mat

def elegir_silla(mat, tipo, partido, lista_partidos):
    #Esta funcion permite que el usuario escoja su asiento, validando que exista y que no este ocupado
    reservada = 'no'
    silla_deseada = 'si'
    while not silla_deseada == reservada:
        silla_deseada=input('Ingrese la silla que desea reservar: ').upper()
        existe = False
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                if (mat[i][j])[:-1] == silla_deseada and (mat[i][j])[-1]=='*':
                        print("That seat is taken, try again: ")
                        existe = True
                        break
                elif mat[i][j] == silla_deseada:
                        mat[i][j] += '*'
                        existe = True
                        reservada = silla_deseada
                        break
            if existe:
                break
        if not existe:
            print('Invalid input, try again: ')
    for i in lista_partidos:
        if i.id == partido:
            if tipo == 'General':
                i.sillas_generales = mat

            else:
                i.sillas_vip =mat
    return lista_partidos, silla_deseada

def validar_entradas(lista_partidos, clientes):
    #Esta funcion valida que las entradas sean reales, verificando que el asiento exista en el estadio, y que nadie mas lo este ocupando
    id = input('Enter your id: ')
    for i in clientes:
        if i.id == id:
            seat = i.seat
            part = i.id_partido
    partido = input('Enter the id of the match you are asisting: ')
    if partido != part:
        print('Invalid match, try again: ')
    aux=0
    while True:
        for i in lista_partidos:
            if i.id == partido:
                game = i
                aux+=1
        if aux!= 1:
            partido = input('Invalid match, try again: ')
        else:
            break
    mat = game.sillas_validadas
    entrada=input('Enter the seat that is on your ticket: ').upper()
    if seat == entrada and part == partido:
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                if (mat[i][j])[:-1] == entrada and (mat[i][j])[-1]=='*':
                    print('That seat is taken, your ticket is false.')
                    print('SECURITYYYYYYYYYYYY!!!!!!')
                    break
                elif mat[i][j] == entrada:
                    mat[i][j] += '*'
                    print('Ticket verified, please come in.')
                    break
        
    else:
        print('That ticket is fake.')
        print('SECURITYYYYYY!!!!!')
    for i in lista_partidos:
        if i.id == partido:
            i.sillas_validadas = mat
    return lista_partidos

def register_restaurants(lista_estadios, lista_restaurantes):
    #Esta funcion crea una lista de todos los restaurantes , y le agrega a cada uno una lista con sus productos
    for i in lista_estadios:
        stadium = i.name
        for j in i.restaurants:
            name = j['name']
            productos = []
            for x in j['products']:
                product = Products(x['name'], x['quantity'], x['price']+x['price']*0.16, x['type'], x['adicional'])
                productos.append(product)
            restaurant = Restaurants(name, stadium, productos)
            lista_restaurantes.append(restaurant)
    return lista_restaurantes
            
def search_restaurants(lista_restaurantes):
    #Esta funcion permite buscar restaurantes
    while True:
        menu = input('Please enter a valid option: \n1 Search by product\n2 Search by type\n3 Search by price\n4Exit\n')
        while not menu.isnumeric() or int(menu) not in range(1,5):
            menu = input('Invalid input, try again: ')
    #Por productos
        if menu == '1':
            products=[]
            for i in lista_restaurantes:
                for j in i.products:
                    aux = 0
                    for x in products:      
                        if j.name == x:
                            aux+=1
                    if aux == 0:
                        products.append(j.name)
            print(products)
            aux = 1
            for i in products:
                    print('Option ', aux, '   ', i)
                    aux+=1
            option = input('Select the option of the product you want: ')
            while not option.isnumeric() or int(option) not in range(len(products)+1):
                option = input('Invalid option, try again: ')
            for i in lista_restaurantes:
                aux2 =0
                for j in i.products:
                    if products[int(option)-1]==j.name:
                        aux2+=1
                if aux != 1:
                    print('At ', i.name)
                    print('')
                for j in i.products:
                    if products[int(option)-1]==j.name:
                        print(j.name, j.price, '$ ')
                        print(' ')
                        print(' ')
            continue
        #por tipo
        if menu == '2':
            tipo = input('Please enter a valid option: \n1 beverages \n2 food\n')
            while not tipo.isnumeric() or int(tipo) not in range(1,3):
                tipo = input('Invalid input, try again: ')
            if tipo == '1':
                tipo = 'beverages'
            if tipo == '2':
                tipo = 'food'
            for i in lista_restaurantes:
                print('')
                print('At ', i.name)
                for j in i.products:
                    if j.type == tipo:
                        print(j.name, j.price, '$')
                    if j.type == tipo:
                        print(j.name, j.price, '$')
                print('')
                print('')
            continue
        #por rango de precio
        if menu == '3':
            min = input('Please enter the minimun price you are looking for: ')
            while not min.isnumeric():
                min=input('Invalid input, try again.')
            max = input('Please enter the maximun price you are looking for: ')
            while not min.isnumeric():
                min=input('Invalid input, try again.')
            for i in lista_restaurantes:
                print('')
                print('At ', i.name)
                for j in i.products:
                    if j.price >= int(min) and j.price <= int(max):
                        print(j.name, j.price, '$')
                print('')
                print('')
            continue
        else:
            break

def ventas_restaurantes(clientes, lista_restaurantes, ticket, cliente, age):
    #Esta funcion se encarga de las compras en los restaurantes
    #Valida que el cliente tengo entrada vip
    #Al final se encarga de imprimir la factura
    aux3=1
    for i in lista_restaurantes:
        print('Option', aux3, '  ', i.name)
        print('')
        aux3+=1
    opt = input('Please enter the restaurant you want to buy from: ')
    while not opt.isnumeric() or int(opt) not in range(len(lista_restaurantes)+1):                
        opt = input('Invalid input, try again: ')
    rest = lista_restaurantes[int(opt)-1]
    productos_comprados=[]
    while True:
        menu = input('Enter a valid option: \n1 Buy\n2 Exit\n')
        while not menu.isnumeric() or int(menu) not in range(1,3):
            menu = input('Invalid input, try again: ')
        if menu=='1':
            cont = 1
            for j in rest.products:
                print('Option ', cont, j.name, j.price, '$ ', j.adicional)
                cont+=1
            product = input('Please select the option you want to buy: ')
            while not product.isnumeric() or int(product) not in range(len(rest.products)+1):
                product = input('Invalid input, try again: ')
            if int(age) < 18 and rest.products[int(product)-1].adicional == 'alcoholic':
                print('Sorry kid, nice try.')
                continue
            if rest.products[int(product)-1].quantity == 0:
               print('Sorry, we are out of ', rest.products[int(product)-1].name)
               continue
            if int(age) < 18 and rest.products[int(product)-1].adicional != 'alcoholic' or int(age) >= 18:
                productos_comprados.append(rest.products[int(product)-1])
                rest.products[int(product)-1].quantity-=1
                lista_restaurantes[int(opt)-1] = rest
                continue    
            if menu == '2':
                clientes = factura(cliente, productos_comprados, clientes)
                break

        return productos_comprados, lista_restaurantes

def factura(cliente, productos_comprados, clientes):
#funcion de factura utilizada en la venta de los restaurantes
    discount=0
    total_sin = 0
    for i in productos_comprados:
        total_sin+=i.price
    divisores = [0]
    suma_divisores = 0
    aux2=int(cliente.id)-1
    while aux2>1:
        if int(cliente.id)%aux2 ==0:
            divisores.append(aux2)
        aux2-=1
    for i in divisores:
        suma_divisores+=i
    if suma_divisores==int(cliente.id):
        discount+=0.15
    else:
        discount+=0
    pago_total = total_sin-total_sin*discount
    print('********RECEIPT********')
    for i in productos_comprados:
        print(i.name, i.price,'$')
    print('Total amount = ', total_sin)
    print('Discount is {}, so you have to pay {}$'.format(discount, pago_total))
    cliente.total_food = pago_total
    for i in clientes:
        if i.id == cliente.id:
            i = cliente
    return clientes

    
def main():
    clientes = []
    lista_restaurantes = []
    lista_equipos = equipos()
    lista_estadios = estadios()
    lista_partidos = partidos(lista_equipos, lista_estadios)
    lista_restaurantes = register_restaurants(lista_estadios, lista_restaurantes)
    while True:
        menu = input('Enter a valid option:\n1 Search matches\n2 Buy ticket\n3 Verify ticket\n4 Search restaurants\n5 Buy food\n6 Exit\n')
        while not menu.isnumeric() or int(menu) not in range(1,7):
            menu = input('Invalid input, try again')
        if menu == '1':
            buscar_partidos(lista_partidos, lista_estadios, lista_equipos)
            continue
        if menu =='2':
            lista_partidos, clientes, cliente = registrar_cliente(lista_partidos, clientes)
            continue
        if menu == '3':
            lista_partidos = validar_entradas(lista_partidos, clientes)
            continue
        if menu == '4':
            search_restaurants(lista_restaurantes)
            continue
        if menu=='5':
            id = input('Please enter your id: ')
            aux = 0
            ticket = 0
            for i in clientes:
                if i.id == id:
                    ticket=i.ticket
                    cliente = i
                    aux+=1
                    age = i.age
            if ticket == 'VIP':
                productos_comprados, lista_restaurantes = ventas_restaurantes(clientes, lista_restaurantes, ticket, cliente, age)
                continue
            else:
                print('Sorry only vip members are allowed to eat.')
                break
        
        else:
            list_cli = []
            for i in clientes:
                cli = {'Nombre': i.name,'Id': i.id,'Age':i.age, 'Id partido': i.id_partido, 'Ticket': i.ticket, 'Seat': i.seat, 'Spend in ticket':i.total_ticket, 'Spend in food': i.total_food}
                list_cli.append(cli)
            list_part = []
            for i in lista_partidos:
                # local, visitor, date, time, Stadium, id, sillas_generales, sillas_vip, sillas_validadas
                part = {'local': i.local, 'Visitor': i.visitor,'date':i.date, 'time':i.time, 'Stadium': i.stadium,'Id': i.id, 'Sillas generales': i.sillas_generales, 'Sillas VIP': i.sillas_vip, 'Entradas verificadas': i.sillas_validadas}
                list_part.append(part)
            list_rest = []
            for i in lista_restaurantes:
                list_products = []
                for j in i.products:
                    product = {'Nombre': j.name, 'Cantidad': j.quantity, 'Precio': j.price, 'Tipo': j.type, 'Adicional': j.adicional}
                    list_products.append(product)
                rest = {'Nombre': i.name,'Stadium': i.stadium, 'Productos': list_products}
                list_rest.append(rest)
            data = {'Clientes': list_cli, 'Partidos': list_part, 'Restaurantes': list_rest}
            with open(r'C:\Users\kikeh\Documents\Proyectodata.json', 'w') as doc:
                json.dump(data, doc, indent=1)
            break
        


main()