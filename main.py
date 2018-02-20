import urllib

import requests
import json



#This sets up the API key from a .txt file in the same directory
#The file has one line in the format of, "API_KEY=XXXXXXXXXXXXXXXXX"
search_file = open("food2fork_API_key.txt", "r")
contents = search_file.read()

if 'API_KEY' in contents:
	
	API_Key = contents[contents.find('=') + 1 :]

search_file.close()


def read_from_cmd():
	'''
	Function that takes in ingredients from command line and places them in a list for later use
	'''
	ingredients = []

	while True:

		text = raw_input("Please enter an ingredient. Type 'exit' when you are satisfied. \n")

		#Base case for exiting this loop, had it convert the user input to lowercase so it wouldn't
		# matter if they entered "exit" or "EXIT" or any other form.
		if text.lower() == "exit":
			break

		ingredients.append(text)
	
	return ingredients

		


def url_builder(request_type, **kwargs):
	'''
	Function that helps build the url that will be used in the
	HTTP request, used kwargs since it lets you handle named arguments 
	in a function, which in turn makes it easier to encode these arguments
	into a url format. 
	'''
	request = { 'key' : API_Key }

	final = request_type + '?' + urllib.urlencode(request)

	dicto = {}

	#Here we add the kwargs values into a dictionary value which will be encoded into a url
	for k, v in kwargs.iteritems():
		dicto[k] = v

	return final + '&' + urllib.urlencode(dicto)


def search_by_trending(q , page ):
	'''
	Function that does a search using the ingredients from a list (q) for trending recipes.
	Returns the number one trending recipe id
	'''

	http_address = 'http://food2fork.com/api/search'

	kwargs = { 'q': ' , '.join(q), 'sort': 't' , 'page': page }

	url = url_builder(http_address, **kwargs)

	content = requests.get(url)

	#I return the first value since that value is the most trending recipe id
	return content.json()['recipes'][0]['recipe_id']

def search_by_rating(q , page ):
	'''
	Function that does a search using the ingredients from a list (q) for high rated recipes.
	Returns the number one rated recipe id
	'''

	http_address = 'http://food2fork.com/api/search'

	kwargs = { 'q': ' , '.join(q), 'sort': 'r' , 'page': page }
	
	url = url_builder(http_address, **kwargs)

	content = requests.get(url)

	#I return the first value since that value is the most highly rated recipe id
	return content.json()['recipes'][0]['recipe_id']

def get_recipe(recipe_id):
	'''
	Function that prints out the ingredients of a recipe
	'''
	http_address = 'http://food2fork.com/api/get'

	kwargs = { 'rId': recipe_id }

	url = url_builder(http_address, **kwargs)

	content = requests.get(url)

	print(content.json()['recipe']['ingredients'])

def get_missing_ingredients(recipe_id, ingredient_list):
	'''
	Function that prints the missing ingredients and current ingredients you have
	'''
	http_address = 'http://food2fork.com/api/get'

	kwargs = { 'rId': recipe_id }

	url = url_builder(http_address, **kwargs)

	content = requests.get(url)

	your_ingredients = []

	print("\n")

	print( "Recipe name: " + content.json()['recipe']['title'])

	print("************************************************* \n")

	print("Missing ingredients: \n")

	count = 0

	while True:

		try:
			current_ingredient = content.json()['recipe']['ingredients'][count]

			for ingredient in ingredient_list:

				'''
				Reasoning behind making these values lowercase is because this code would miss a case
				in which an input ingredient would be 'Milk' and the recipe ingredient would be '2/3 cup milk'
				'''
				if ingredient.lower() in current_ingredient.lower():
					
					

					if ingredient.lower() == len(current_ingredient.lower()):
						
						your_ingredients.append( "YOU HAVE THIS INGREDIENT: " + current_ingredient )
					else:
						
						your_ingredients.append( "YOU HAVE A SIMILAR INGREDIENT: " + current_ingredient )

					

					break

				'''
				Reasoning behind this case is for where the input ingredient would be 'anchovies' and the recipe ingredient
				would be 'anchovy', so here we are checking for the plural case
				'''
				if "ies" in ingredient.lower():

					#temp is basically the ingredient with the "ies" shaved off the end and a 'y' is added to it, 
					# "anchovies" -> "anchovy"
					temp = ingredient.lower()[ :ingredient.lower().rfind("ies") ] + 'y'
					
					if temp.lower() in current_ingredient.lower():
						
						

						if temp.lower() == len(current_ingredient.lower()):
							
							your_ingredients.append( "YOU HAVE THIS INGREDIENT: " + current_ingredient )
						else:
							
							your_ingredients.append( "YOU HAVE EXCESS OF THIS INGREDIENT: " + current_ingredient )
						

						break

				'''
				Reasoning behind this case is for where the input ingredient would be 'eggs' and the recipe ingredient
				would be 'egg', now I put this if statement after the previous one just in case there's an ingredient 
				like 'anchovies', but we are still checking for the plural case
				'''
				if ingredient.lower()[ len( ingredient.lower() ) - 1 ] == 's':
					
					#temp is basically the ingredient with the 's' shaved off the end, "eggs" -> "egg"
					temp = ingredient.lower()[ : len(ingredient.lower()) - 1 ] 

					if temp.lower() in current_ingredient.lower():
						
						

						if temp.lower() == len(current_ingredient.lower()):
							
							your_ingredients.append( "YOU HAVE THIS INGREDIENT: " + current_ingredient )
						else:
							
							your_ingredients.append( "YOU HAVE EXCESS OF THIS INGREDIENT: " + current_ingredient )
						

						break


				'''
				Case for which ingredient isn't in the list generated by the user input.
				Checking for if the current ingredient is at the end of the list, and isn't in the list because 
				if say the ingredient was at the beginning of the list, it would keep printing the same ingredient for 
				the remainder of the list.
				'''
				if ingredient == ingredient_list[len(ingredient_list) - 1] and (ingredient.lower() not in current_ingredient.lower()) :
					print(current_ingredient)
			
			count += 1

		except IndexError:
			break

	print("\n")
	print("Your ingredients: \n")

	for ingredient in your_ingredients:
		print(ingredient)
	print("\n")
def runner():
	'''
	This function simply does all the magic, basically gets the ingredients from command line, 
	searches for a recipe that has some of those ingredients, and prints the missing ingredients
	from the recipe
	'''
	ingredient_list = read_from_cmd()

	'''
	This try-except block is for the case in which if the search for a trending recipe returns
	nothing, so in that case I search for a highly rated recipe instead
	'''
	try:
		recipe_id = search_by_trending(ingredient_list, '1')
	
	except IndexError:
		recipe_id = search_by_rating(ingredient_list, '1') 

	get_missing_ingredients( recipe_id, ingredient_list )


runner()