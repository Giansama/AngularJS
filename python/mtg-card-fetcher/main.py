import requests
#import json

def get_card(card_name):
    url = "https://api.scryfall.com/cards/named?exact="+card_name
    r = requests.get(url)
    j = r.json()
    
    print("\n")
    if j['layout'] == "transform":
        faces = j['card_faces']
        for x in range(2):
            print("\t",faces[x]['name'],"\n",
                    faces[x]['type_line'],"\n",
                    faces[x]['oracle_text'],"\n",
                    "Imagem: ",faces[x]['image_uris']['normal'],"\n")
    elif j['layout'] == "split" or j['layout'] == "flip":
        faces = j['card_faces']
        for x in range(2):
            print("\t",faces[x]['name'],"\n",
                    faces[x]['type_line'],"\n",
                    faces[x]['oracle_text'],"\n")
        print("Imagem: ",j['image_uris']['normal'])
    else:
        print("\t",j['name'],"\n",
                j['type_line'],"\n",
                j['oracle_text'],"\n",
                "Imagem: ",j['image_uris']['normal'])
    
    print("\nLegalidade: ")
    for key in j['legalities']:
        if j['legalities'][key] == "legal":
            print(key, end = " ")

def fetch_list(search_string):
    url = "https://api.scryfall.com/cards/autocomplete?q="+search_string
    r = requests.get(url)
    
    r_list = r.json()['data']
    for x in range(len(r_list)):
        print(x+1," : ",r_list[x])
    
    select_card = int(input("Select Card: "))
    if select_card > 0 and select_card < len(r_list)+1:
        get_card(r_list[select_card-1])
    else:
        print("\n\t\tPrograma Encerrado...")
        exit(-1)
    
def main():
    search_input = input("Entre no com o nome da carta a pesquisar: ")
    fetch_list(search_input)

main()
