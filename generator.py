import json
import secrets

def main():
	while True:
		command = input('Enter a command; "q" to quit, or "help" for a list of commands: ')
		command = command.lower().strip().split(' ')
		if command[0][0] == 'q':
			break
		elif command[0] == 'generate':
			passphrases = generate(int(command[1])) # Todo: handle index out of range, etc.
			for i in range(len(passphrases)): # ensures each passphrase prints to a new line
				passphrases[i] += '\n'
			file_out = open(command[2], 'a')
			file_out.writelines(passphrases)
			file_out.close()
		elif command[0] == 'print':
			passphrases = generate()
			print(passphrases[0])
		elif command[0] == 'config':
			config()
		elif command[0] == 'help':
			for k in command_list:
				print(k+':',command_list[k])

def generate(number=1):
	passphrases = list()
	words_length = len(words)
	for n in range(number):
		passphrase = str()
		while True: # break conditions are handled within the loop
			new_word = secrets.choice(words).capitalize()
			if len(passphrase) + len(new_word) <= settings['maxlength']-2: # ensures passphrase will be at most maxlength once the final separator and ending number are added
				passphrase += new_word
				passphrase += secrets.choice(settings['separators'])
			elif len(passphrase) <= settings['minlength']-2: # ensures passphrase will be at least minlength once the final separator and ending number are added
				continue
			else:
				passphrase += str(secrets.randbelow(10))
				break
		passphrases.append(passphrase)
	return passphrases

def config():
	while True: # Todo: add a case that reverts a value to the default
		print('Current settings:')
		for k in settings:
			print(k+':',settings[k])
		command = input('Configure settings; "q" to quit, or "help" for usage information: ')
		command = command.lower().strip().split(' ')
		if command[0] in ['minlength', 'maxlength', 'maxwordlength']:
			new_value = int(command[1])
			if new_value > 0:
				command[1] = new_value
			else:
				print('Please give a positive number!')
		if command[0][0] == 'q':
			break
		elif command[0] == 'help':
			print('Configuration usage: <setting name> <setting value>')
			print('For instance, to change "minlength" to 12, type: "minlength 12"')
		elif command[0] == 'maxwordlength':
			settings[command[0]] = command[1]
			words = build_vocab(settings['maxwordlength'])
		elif command[0] in settings:
			settings[command[0]] = command[1]
		else:
			print('Please enter a valid setting.')
	command = input('Save configuration changes? y/n: ').lower()
	if command[0] == 'y':
		write_json('config.json', settings)

def build_vocab(length): # processes list of words to be sufficiently short to generate memorable passphrases
	words_all = read_json('words_dictionary.json')
	words = list()
	for k in words_all:
		if len(k) <= length:
			words.append(k)
	return words

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def write_json(path, data):
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2)

default_settings = {'minlength':8, 'maxlength':20, 'maxwordlength':8, 'separators':'-!#$%^&*'} # Todo: Elaborate on what settings the user will need. Add: Default directory; name of config file?; 

try:
	settings = read_json('config.json')
except FileNotFoundError:
	settings = default_settings # ensures program will act normally on first run
	write_json('config.json', settings)

command_list = {'generate':'generate <number of passphrases> <path.txt> append generated passphrases to path.txt', 'print':'print a single passphrase to terminal', 'config':'configure program settings', 'help':'list all commands', 'q':'quit program'}
config_list = {'minlength':'minimum passphrase length', 'maxlength':'maximum passphrase length', 'maxwordlength':'the maximum allowed length per word', 'separators':'characters to separate words in a passphrase'}
words = build_vocab(settings['maxwordlength'])

main()