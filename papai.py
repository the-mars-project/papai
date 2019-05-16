#!/usr/bin/env Python3
# -*- Coding: UTF-8 -*-


import discord, json, subprocess, time, sys, os

if sys.version_info[0] != 3 or sys.version_info[1] != 6:
	raise Exception('Error: Requires Python3.6')


class Server(object):

	def __init__(self):
		print('starting MC server')
		self.process = subprocess.Popen(['java', '-Xmx7068M', '-Xms7068M', '-jar', 'server.jar', 'nogui'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		time.sleep(20)
		
	
	def Keepalive(self):
	
		if self.process.poll() is None:
			print('Server process exists.')
			return True
		else:
			print('Server process appears to have exited.')
			for i in range(1,10):
				if self.process.poll is not None:
					self.process = subprocess.Popen(['java', '-Xmx7068M', '-Xms7068M', '-jar', 'server.jar', 'nogui'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					time.sleep(20)
				else:
					return True
				print('Server could not be started.')
			return False
			
	
	def Send_message(self, message):
		try:	
			time.sleep(1) # added to be graceful to the process.
			self.process.stdin.write(message):
			self.process.flush()
		except NameError:
			#placeholder error, I don't know what writing to a locked buffer will call.
			pass


def Whitelist(Instance, id, name):

	with open('_whitelist.json', 'wr+') as whitelist:
		if os.path.isfile('./_whitelist.json'):
			whitedict = dict(json.loads(whitelist))
		else:
			whitedict = {}
		if id in whitedict:
			Instance.Send_message('whitelist remove {}'.format(whitedict[id]))
		whitedict.update({id:name})
		Instance.Send_message('whitelist add {}'.format(name))
		json.dump(whitedict, whitelist)
		
		
def Discord(Instance):

	admins = [] # placeholder list till I can figure out how to check admins properly.
	Disclient = discord.Client()
	
	
	@Disclient.event
	async def on_ready(self):
		Instance.Send_Message('say GoldyBlocks has initialised.')
	
	
	@Disclient.event
	async def on_message(message):
		if message.author == Disclient.user:
			return
		if message.channel == 'subscribers':
			if message.content.startswith('!mc'):
				name = str(message.content).split()[1]
				Instance.Whitelist(Instance, message.author.id, name)
				await message.channel.send('{}, you have been whitelisted on 45.63.29.171 as {}'.format(message.author, name))
			if str(message.content) == '!ping'
				if Instance.Keepalive is True:
					await message.channel.send('The Server appears to be online. \nIP: 45.63.29.171 \nAsk an Admin to issue the Restart command via discord.')
				if Instance.Keepalive is False:
					await message.channel.send('The Server is offline, and could not be started. Please @ Papa rich.')
			if str(message.content) == '!restart':
				if message.author.id in admins:
					await message.channel.send('Attempting to restart the server gracefully.')
					Instance.Send_message('say Server is going to be restarted in 15 seconds. Please get safe.')
					time.sleep(15)
					Instance.Send_message('stop')
					time.sleep(20)
					Instance.Keepalive()
					await message.channel.send('If the server is not accessible now, there is a bigger issue. @ Papa Rich.')
	Disclient.run('token')
	
	
def main():
	Instance = Server()
	if Instance.Keepalive():
		ChatManager = Discord(Instance)
		print('!!! Hey I think it doesnt stop')
	else:
		raise Exception('MC Server did not start successfully.')