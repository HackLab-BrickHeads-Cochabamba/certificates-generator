import json
import copy
from unidecode import unidecode

certificate = None

def sluglify(name):
  name = unidecode(name)
  name = name.strip().split(' ')
  return '-'.join(word.strip() for word in name)

with open('./data/certificate.svg','r') as file:
  certificate = file.read()

with open('./data/data.json','r', encoding='utf-8') as file:
  data = file.read()
  data = json.loads(data)
  for course in data:
    template = copy.copy(certificate)
    template = template.replace(
      '::INSTRUCTOR_NAME::',
      course['instructor_name']
    )
    template = template.replace('::SUBJECT::', course['name'])
    template = template.replace('::DURATION::', course['duration'])
    template = template.replace('::DATE_START::', course['date_start'])
    template = template.replace(
      '::DATE_END::', 
      course['date_end'] if course['date_end'] else ''
    )

    for student in course['students']:
      last_template = copy.copy(template)
      last_template = last_template.replace('::NAME::', student)
      file_name = sluglify(student)

      with open(
        './out/{}_{}.svg'
        .format(file_name, sluglify(course['name']).replace('/','-'))
        .replace(' ',''), 
        'w'
      ) as file:
        file.write(last_template)
        file.close()
