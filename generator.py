def geraPrimos(x):
    lista = list(range(x))
    
    for p in lista[2:]:
        primo = True
        
        for q in lista[2:p]:
            if p%q == 0:
                primo = False
        
        if primo:
            yield p

while True:
    try:
        limite = int(input("\n\nDigite o numero limite\npara cálcular os primos: "))
        break
    except:
        input("Entrada inválida!")
listaPrimos = list(geraPrimos(limite))
print("\nOs primos até o numero {0} são:\n{1}".format(limite,listaPrimos))


