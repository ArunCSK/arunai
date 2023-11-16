import re

text = '--adc_dfge)jk#4234$dddh@!^dadg'
pattern = '--'

# find_all_list = re.match(pattern,text)
# print(find_all_list)

text_replaced = re.sub(pattern,'', text)
print(text_replaced)
# search_all_list = re.search(pattern,text)
# print(search_all_list)

