import pandas as pd
import xmltodict
import xml.etree.ElementTree as ET

def xml_to_csv(file_path, output_path):
    with open(file_path, 'r') as file:
        xml_content = file.read()
        data = xmltodict.parse(xml_content)

    code_lists = data["mes:Structure"]["mes:Structures"]['str:Codelists']['str:Codelist']

    output = {}

    for i in range(len(code_lists)):
        list = code_lists[i]
        name_of_list = list['com:Name']['#text']
        print(name_of_list)

        codelist_df = {}
        code_data = list['str:Code']
        for x in range(len(code_data)):
            df_result = pd.DataFrame({
                'list_name': name_of_list,
                'urn': code_data[x].get('@urn', 'N/A'),
                'id': code_data[x].get('@id', 'N/A'),
                'name': code_data[x].get('com:Name', {}).get('#text', 'N/A'),
                'desc': code_data[x].get('com:Description', {}).get('#text', 'N/A')
            }, index=[1])

            codelist_df[x] = df_result
        
        codelist_df_combined = pd.concat(codelist_df.values())
        output[i] = codelist_df_combined

    result = pd.concat(output.values())
    result.columns = ["codelist_name", "urn", "notation", "label", "description"]
    result.to_csv(output_path, encoding='utf-8')

if __name__ == "__main__":
    xml_to_csv(file_path="/Users/abdulkasim/Documents/data_ingestion_projects/national-accounts/xml/STRUCTURE.xml", output_path="src/CodeLists.csv")