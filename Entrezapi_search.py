import sys #Permite interação com o sistema
import urllib.request #Permite buscar dados a partir de URLs
import urllib.parse # Permite realizar modificações e operações em URLs
import xml.etree.ElementTree as xml_mod #Facilita a manipulação de documentos xml

def perform_search(database, search_term):
    """
    Procura por sequencias na base de dados especificada usando os termos obtidos através do terminal.
    Retorna IDs, WebEnv, e QueryKey para os resultados de pesquisa.
    """
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_parameters = {
        "db": database,
        "term": search_term,
        "usehistory": "y",
        "retmode": "xml"
    }
    search_response = urllib.request.urlopen(search_url + "?" + urllib.parse.urlencode(search_parameters))
    search_data = search_response.read()
    search_tree = xml_mod.fromstring(search_data)
    id_list = [id_elem.text for id_elem in search_tree.findall(".//Id")]
    webenv = search_tree.find(".//WebEnv").text
    query_key = search_tree.find(".//QueryKey").text
    return id_list, webenv, query_key

def fetch_sequences(database, id_list, webenv, query_key):
    """
    Busca sequencias da base de dados especificada, tendo em conta a lista de ids.
    """
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    fetch_parameters = {
        "db": database,
        "query_key": query_key,
        "WebEnv": webenv,
        "id": ",".join(id_list),
        "rettype": "fasta",
        "retmode": "text"
   }
    fetch_response = urllib.request.urlopen(fetch_url + "?" + urllib.parse.urlencode(fetch_parameters))
    fasta_data = fetch_response.read()
    return fasta_data

def print_sequences(fasta_data):
    """
    Print das sequencias obtidas através do def fetch no formato fasta"
    """
    sys.stdout.buffer.write(fasta_data)
def main():
    if len(sys.argv) < 3:
        print("Usage: python3 script.py <database> ""search_term"" ")
        sys.exit(1)
    database = sys.argv[1]
    search_term = sys.argv[2]
    id_list, webenv, query_key = perform_search(database, search_term)
    fasta_data = fetch_sequences(database, id_list, webenv, query_key)
    print_sequences(fasta_data)

if __name__ == "__main__":
    main()
