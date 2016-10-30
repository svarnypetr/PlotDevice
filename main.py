# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 13:45:13 2016

@author: bento

Idea: 
- import data about movies
- calculate probability distribution of properties
-- never movies are more important by factor f
- "predict" new movie
-- simple random number choice

"""

import random

from collections import Counter

import data.movies as m


def get_var_list(data, var, base, factor):
    """
    Gets a list of values for given movie variable.
    """
    var_all = []    
    for a_movie in data:
        var_all.extend((a_movie[var])*base)
        base += factor
    return var_all


def get_var(data, var, base, factor):
    """
    Returns a random value from the data for given var.
    """
    a_list = get_var_list(data, var, base, factor)
    return random.choice(a_list)


def get_var_count_list(data,var,base,factor):
    """
    Returns the a list of how many times a movie had a given a variable.
    """
    var_count_list = []
    for a_movie in data:
        var_count_list.extend([len(a_movie[var])]*base)
        base += factor
    return var_count_list

    
def get_simple_value(data,var,base,factor):
    var_count = random.choice(get_var_count_list(data,var,base,factor))
    result_list = []
    for i in range(var_count):
        result_list.append(get_var(data, var, base, factor))
    return list(set(result_list))

def get_role_var(data,role_var,base,factor):
    role_var_list = []
    role_var_count = []
    for a_movie in data:
        for a_role in a_movie['main']:
                role_var_count.extend([len(a_role[role_var])]*base)
                role_var_list.extend([a_role[role_var]]*base)
        base += factor
    if role_var == 'char':
        role_var_list = sum(role_var_list,[])
    return (role_var_list,role_var_count)

def get_simple_roles(data,main_num,base, factor):
    roles = []
    for a_role in range(int(main_num[0])):
        actor = {}
        gender = random.choice(get_role_var(data,'gender',base,factor)[0])
        age = random.choice(get_role_var(data,'age',base,factor)[0])
        char = random.choice(get_role_var(data,'char',base,factor)[0])
        actor.update({
            'gender':gender,
            'age':age,
            'char':char})
        roles.append(actor)
    return roles
# {'gender': "zena", 'age': 24, 'char': ["knihovnice"]}



def get_most_roles(data,main_num,base, factor):
    roles = []
    for a_role in range(int(main_num[0])):
        actor = {}
        gender = Counter(
                    get_role_var(data,'gender',base,factor)[0]
                ).most_common(1)[0][0]
        age = Counter(
                get_role_var(data,'age',base,factor)[0]
                ).most_common(int(main_num[0]))[a_role][0]
        char = Counter(
                get_role_var(data,'char',base,factor)[0]
                ).most_common(int(main_num[0]))[a_role][0]
        actor.update({
            'gender':gender,
            'age':age,
            'char':char})
        roles.append(actor)
    return roles


def get_most_value(data,var,base,factor):
    most_value_list = []
    var_count = Counter(get_var_count_list(data,var,base,factor)).most_common(1)[0][0]
    for i in range(var_count):
        most_value = Counter(get_var_list(data,var,base,factor)).most_common(var_count)[i][0]
        most_value_list.append(most_value)
    return most_value_list


def generate_random_new_movie(data, base=1, factor=0):
    mov = {}
    
    # Solve actors
    main_num = get_simple_value(data,"main_num", base, factor)
    main = get_simple_roles(data,main_num,base, factor)
    
    # Update mov variables
    mov.update({
                'main_num': main_num,
                'main': main,
            	'support': get_simple_value(data,"support", base, factor),
            	'genre': get_simple_value(data,"genre", base, factor),
            	'period': get_simple_value(data,"period", base, factor),
            	'location': get_simple_value(data,"location", base, factor),
            	'places': get_simple_value(data,"places", base, factor),
            	'theme': get_simple_value(data,"theme", base, factor),
            	'music': get_simple_value(data,"music", base, factor)      
                })
    return mov

def generate_most_probable_movie(data,base=1, factor=0):
    mov = {}
    
    # Solve actors
    main_num = get_most_value(data,"main_num", base, factor)
    main = get_most_roles(data,main_num,base, factor)
    
    # Update simple variables
    mov.update({
                'main_num': main_num,
                'main': main,
            	'support': get_most_value(data,"support", base, factor),
            	'genre': get_most_value(data,"genre", base, factor),
            	'period': get_most_value(data,"period", base, factor),
            	'location': get_most_value(data,"location", base, factor),
            	'places': get_most_value(data,"places", base, factor),
            	'theme': get_most_value(data,"theme", base, factor),
            	'music': get_most_value(data,"music", base, factor)      
                })
    return mov

with open("output.txt", "w") as myfile:
    myfile.write("Nejpravdepodobnejsi film:\n\n")
    mov = generate_most_probable_movie(m.movies, 10, 1)
    myfile.write("Obdobi: "+str(mov['period'])+"\n")
    myfile.write("Zanr: "+str(mov['genre'])+"\n")
    myfile.write("Tema: "+str(mov['theme'])+"\n")
    myfile.write("Misto: "+str(mov['location'])+"\n")
    myfile.write("Sceny: "+str(mov['places'])+"\n")
    myfile.write("Hudba: "+str(mov['music'])+"\n")
    myfile.write("Vedlejsi postavy: "+str(mov['support'])+"\n")
    myfile.write("Pocet hlavnich postav: "+str(mov['main_num'])+"\n\n")
    i = 1
    for an_actor in mov['main']:
        myfile.write(str(i)+". hlavni postava:\n")
        myfile.write("\tPohlavi: "+an_actor['gender']+"\n")
        myfile.write("\tVek: "+an_actor['age']+"\n")
        myfile.write("\tCharakter: "+an_actor['char']+"\n")
        i += 1
    myfile.write("\n\n")

    myfile.write("-------------------------------------------\n")
    myfile.write("Statisticky generovane filmy\n")
    myfile.write("-------------------------------------------\n")
    
    for iteration in range(20):
        myfile.write("----"+str(iteration+1)+". film----\n\n")
        mov = generate_random_new_movie(m.movies, 10, 1)
        myfile.write("Obdobi: "+str(mov['period'])+"\n")
        myfile.write("Zanr: "+str(mov['genre'])+"\n")
        myfile.write("Tema: "+str(mov['theme'])+"\n")
        myfile.write("Misto: "+str(mov['location'])+"\n")
        myfile.write("Sceny: "+str(mov['places'])+"\n")
        myfile.write("Hudba: "+str(mov['music'])+"\n")
        myfile.write("Vedlejsi postavy: "+str(mov['support'])+"\n")
        myfile.write("Pocet hlavnich postav: "+str(mov['main_num'])+"\n\n")
        i = 1
        for an_actor in mov['main']:
            myfile.write(str(i)+". hlavni postava:\n")
            myfile.write("\tPohlavi: "+an_actor['gender']+"\n")
            myfile.write("\tVek: "+an_actor['age']+"\n")
            myfile.write("\tCharakter: "+an_actor['char']+"\n")
            i += 1
        myfile.write("\n\n")
 