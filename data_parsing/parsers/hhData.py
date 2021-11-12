import json
import pandas as pd
import re
import numpy as np
from collections import Counter
from matplotlib import pyplot as plt
from tqdm import tqdm

class hhData:

    specializations = []
    specializations_id = set()

    profarea_dict = {}
    specializations_dict = {}

    profarea_counts = Counter()
    specializations_counts = Counter()

    data_transformed = []

    all_specializations = {}

    def __init__(self):
        specializations_list = [('1.10', 'Web мастер'),
                 ('1.110', 'Компьютерная безопасность'),
                 ('1.117', 'Тестирование'),
                 ('1.203', 'Передача данных и доступ в интернет'),
                 ('1.221', 'Программирование, Разработка'),
                 ('1.270', 'Сетевые технологии'),
                 ('1.272', 'Системная интеграция'),
                 ('1.273', 'Системный администратор'),
                 ('1.274', 'Системы автоматизированного проектирования'),
                 ('1.277', 'Сотовые, Беспроводные технологии'),
                 ('1.295', 'Телекоммуникации'),
                 ('1.296', 'Технический писатель'),
                 ('1.3', 'CTO, CIO, Директор по IT'),
                 ('1.327', 'Управление проектами'),
                 ('1.395', 'Банковское ПО'),
                 ('1.400', 'Оптимизация сайта (SEO)'),
                 ('1.420', 'Администратор баз данных'),
                 ('1.475', 'Игровое ПО'),
                 ('1.50', 'Системы управления предприятием (ERP)'),
                 ('1.536', 'CRM системы'),
                 ('1.89', 'Интернет'),
                 ('1.9', 'Web инженер')]
        self.specialization = [i[1] for i in specializations_list]
        self.specializations_id = set([i[0] for i in specializations_list])
    
    def transform(self, data_row):

        data_dict = {}
        if (len(set([i['id'] for i in data_row['specializations']]) & self.specializations_id)):
    
    
            specializations_set = set()
            profarea_name_set = set()
    
            for i in data_row['specializations']:
            
                profarea_name_set.add(i['profarea_id'])
                specializations_set.add(i['id'])
            
                self.profarea_dict[i['profarea_id']] = i['profarea_name']
                self.specializations_dict[i['id']] = i['name']
            
                self.profarea_counts[i['profarea_name']] += 1
                self.specializations_counts[i['name']] += 1
    
    
            data_dict = { 'name' : data_row['name'],
                      'area' : data_row['area']['name'],
                      'key_skills' : [i['name'] for i in data_row['key_skills']],
                      'published_at' : data_row['published_at'],
                      'specializations' : list(specializations_set),
                      'profarea_name' : list(profarea_name_set)}
        
        return data_dict

    def load_data(self, files):
    
        for file in tqdm(files):
            data_file = open("hh_data/" + file, 'r', encoding='utf-8')
            data = data_file.readlines()
            data_file.close()

            for line in data:

                data_line = ''
                try:
                    data_line = json.loads(line)
                except:
                    print('error while open json')
                if data_line:
                    try:
                        new_row = self.transform(data_line)
                        if (new_row):
                            self.data_transformed.append(new_row)
                    except:
                        print('error while parsing')
                    
        return self.data_transformed
