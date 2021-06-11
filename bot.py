import discord
import os

class SplitBot(discord.Client):
  async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))

  async def on_message(self, message):
    print('Message from {0.author}: {0.content}'.format(message))
    if message.author == self.user:
      return
    await message.channel.send(message.content)

def main():
  client = SplitBot()
  client.run(os.getenv('TOKEN'))

if __name__ == '__main__':
  main()
