from flask import Flask, request

app = Flask(__name__) #apelam constructorul clasei Flask

@app.route("/") #  @app.route e un decorator - un decorator adauga functionalitate functiilor, asta se foloseste pentru flask
                #intre paranteze punem route-ul de la web service ul pe care il pornim(cum sunt pe siteuri /home spre ex)
def first_function():
    return{"message": "Hello World!"}

@app.route("/home", methods=['GET', 'POST']) #parametrul default pt methods este GET, daca vrei sa mearga alte tipuri
                                                #           de request-uri trebuie sa specificam tipul pe care il vrem
                                              #                acum se poate doar GET si POST

def second_function():
    print(request.method) #o sa ne apara in consola din python ce metoda am utilizat - evident o sa ne apara GET pentru
                            # ca nu am creat nimic, nu avem cum sa utlizam POST, pentru ca in momentul in care intram pe link apare doar mesajul si atat
    return {"message": "Daca rulam link-ul din consola iar dupa adaugam route-ul home va aparea mesajul asta"}

#cand o sa lucram cu html o sa dam return render_template("numele_templateului")
#exemplu: facem o functie care sa verifice daca parola este corecta, daca este va fi redirectionat catre un anumit template,
#   iar daca nu catre altul unde se afla un mesaj ca a gresit parola



if __name__ == '__main__':
    app.run() #aici rulam aplicatia noastra








