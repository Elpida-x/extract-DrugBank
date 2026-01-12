import xml.etree.ElementTree as ET
import csv
import os
import re

def clean_text(text):
    if text:
        return re.sub(r'\s+', ' ', text).strip()
    return None

def get_primary_drugbank_id(drug_elem):
    db_id = None
    found_ids = []
    
    for child in drug_elem:
        if child.tag.endswith('drugbank-id'):
            found_ids.append(child)
            
    for eid in found_ids:
        if eid.get('primary') == 'true':
            db_id = eid.text
            break
            
    if not db_id and found_ids:
        db_id = found_ids[0].text
    
    return db_id

def extract_basic_drug_info(drug_elem):
    data = {}
    data['drugbank-id'] = get_primary_drugbank_id(drug_elem)
    
    if not data['drugbank-id']:
        return None

    name_elem = None
    desc_elem = None
    
    for child in drug_elem:
        if child.tag.endswith('name'):
            name_elem = child
        elif child.tag.endswith('description'):
            desc_elem = child
            
    data['name'] = clean_text(name_elem.text) if name_elem is not None else None
    data['description'] = clean_text(desc_elem.text) if desc_elem is not None else "N/A"
    
    return data

def extract_detailed_drug_info(drug_elem):
    data = {}
    data['drugbank-id'] = get_primary_drugbank_id(drug_elem)
    
    if not data['drugbank-id']:
        return None
        
    # Fields to extract directly
    target_tags = {
        'indication', 'pharmacodynamics', 'mechanism-of-action', 
        'toxicity', 'metabolism', 'absorption', 'route-of-elimination'
    }
    
    # Initialize target fields
    for tag in target_tags:
        data[tag] = "N/A"
    data['synonyms'] = "N/A"

    for child in drug_elem:
        # Simple tag matching ignoring namespace
        tag_name = child.tag
        if '}' in tag_name:
            tag_name = tag_name.split('}', 1)[1]
            
        if tag_name in target_tags:
            data[tag_name] = clean_text(child.text) or "N/A"
        elif tag_name == 'synonyms':
            syn_list = []
            for syn in child:
                if syn.text:
                    syn_list.append(clean_text(syn.text))
            if syn_list:
                data['synonyms'] = " | ".join(syn_list)

    return data

def extract_drug_interactions(drug_elem):
    # This function is different because it returns a LIST of interactions, not a single dictionary
    # The parent drug ID is the "source" drug
    parent_id = get_primary_drugbank_id(drug_elem)
    
    if not parent_id:
        return []
        
    interactions = []
    
    # Locate <drug-interactions>
    interactions_group = None
    for child in drug_elem:
        if child.tag.endswith('drug-interactions'):
            interactions_group = child
            break
            
    if interactions_group is not None:
        for interaction in interactions_group:
            # Each interaction has <drugbank-id>, <name>, <description>
            inter_data = {
                'drugbank-id': parent_id, # The active drug ID
                'interaction-drugbank-id': 'N/A', # The interacting drug's ID
                'name': 'N/A',
                'description': 'N/A'
            }
            
            for field in interaction:
                tag_name = field.tag
                if '}' in tag_name:
                    tag_name = tag_name.split('}', 1)[1]
                
                if tag_name == 'drugbank-id':
                    inter_data['interaction-drugbank-id'] = clean_text(field.text)
                elif tag_name == 'name':
                    inter_data['name'] = clean_text(field.text)
                elif tag_name == 'description':
                    inter_data['description'] = clean_text(field.text)
            
            interactions.append(inter_data)
            
    return interactions

def process_xml(xml_file, output_csv, extract_func, fieldnames, is_list_output=False):
    if not os.path.exists(xml_file):
        print(f"Error: File {xml_file} not found.")
        return

    context = ET.iterparse(xml_file, events=('end',))
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        count = 0
        drug_count = 0
        
        for event, elem in context:
            if elem.tag.endswith('drug'):
                if elem.get('type'):
                    drug_count += 1
                    extracted_data = extract_func(elem)
                    
                    if is_list_output:
                        if extracted_data:
                            for row in extracted_data:
                                writer.writerow(row)
                                count += 1
                    else:
                        if extracted_data:
                            writer.writerow(extracted_data)
                            count += 1
                elem.clear()
        
        if is_list_output:
             print(f"Extraction complete for {output_csv}. Processed {drug_count} drugs, found {count} total rows.")
        else:
             print(f"Extraction complete for {output_csv}. {count} drugs processed.")

def process_basic_drug_xml(xml_file, output_csv):
    fieldnames = ['drugbank-id', 'name', 'description']
    process_xml(xml_file, output_csv, extract_basic_drug_info, fieldnames)

def process_detailed_drug_xml(xml_file, output_csv):
    fieldnames = [
        'drugbank-id', 'synonyms', 'indication', 'pharmacodynamics', 
        'mechanism-of-action', 'toxicity', 'metabolism', 
        'absorption', 'route-of-elimination'
    ]
    process_xml(xml_file, output_csv, extract_detailed_drug_info, fieldnames)

def process_drug_interactions_xml(xml_file, output_csv):
    # Note: Added 'interaction-drugbank-id' to distinguish from parents
    fieldnames = ['drugbank-id', 'interaction-drugbank-id', 'name', 'description']
    process_xml(xml_file, output_csv, extract_drug_interactions, fieldnames, is_list_output=True)

if __name__ == "__main__":
    input_xml = 'full database.xml'
    
    # Process BasicDrug
    # print("Processing BasicDrug...")
    # process_basic_drug_xml(input_xml, 'BasicDrug.csv')
    
    # Process DetailedDrug
    # print("Processing DetailedDrug...")
    # process_detailed_drug_xml(input_xml, 'DetailedDrug.csv')
    
    # Process DrugInteractions
    print("Processing DrugInteractions...")
    process_drug_interactions_xml(input_xml, 'DrugInteractions.csv')
