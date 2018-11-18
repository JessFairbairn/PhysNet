import wikipediaapi as wp

wiki_wiki = wp.Wikipedia('en')
physics_cat = wiki_wiki.page("Category:Physics")

big_list=[]
articles_list = []

def recursively_sort_category(cat: wp.WikipediaPage, level:int):
    if level >= 3:
        return

    for name in cat.categorymembers:
        if name.startswith('Category:') and not name.endswith('templates'):
            recursively_sort_category(cat.categorymembers[name], level +1)

            big_list.append(name.split(':')[1])
        else:
            articles_list.append(name)

recursively_sort_category(physics_cat, 1)

with open('physics_articles.txt','w') as mah_file:
    for cat in articles_list:
        mah_file.write(cat + '\n')