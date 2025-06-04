import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from pathlib import Path

# Configuração segura do .env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print("❌ ERRO: Token não encontrado no arquivo .env")
    print("Verifique se:")
    print("1. O arquivo .env existe na mesma pasta")
    print("2. Contém uma linha como: DISCORD_TOKEN=seu_token_aqui")
    exit(1)


intents = discord.Intents.all()  # Ativa todos os intents necessários

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    case_insensitive=True
)

temp_channels = {}

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user.name}')
    print(f'🆔 ID do Bot: {bot.user.id}')
    print(f'📋 Servidores: {len(bot.guilds)}')
    print('------')

@bot.event
async def on_voice_state_update(member, before, after):
    # ID do canal de criação - substitua pelo SEU ID REAL
    CREATION_CHANNEL_ID = 1372061933183701062
    
    # Usuário entrou em um canal
    if not before.channel and after.channel:
        if after.channel.id == CREATION_CHANNEL_ID:
            try:
                guild = member.guild
                category = after.channel.category
                
                new_channel = await guild.create_voice_channel(
                    name=f'🔊 {member.display_name}',
                    category=category,
                    user_limit=7,
                    reason=f"Canal criado por {member}"
                )
                
                await new_channel.set_permissions(
                    member,
                    manage_channels=True,
                    connect=True,
                    speak=True,
                    reason="Dono do canal temporário"
                )
                
                await member.move_to(new_channel)
                temp_channels[new_channel.id] = member.id
                
                print(f'🎚 Canal criado: {new_channel.name}')
                
            except Exception as error:
                print(f'❌ Erro ao criar canal: {error}')
                try:
                    await member.send('⚠️ Não consegui criar seu canal de voz!')
                except:
                    pass
    
    # Verifica canais vazios
    if before.channel and before.channel.id in temp_channels:
        if not before.channel.members:
            try:
                await before.channel.delete()
                del temp_channels[before.channel.id]
                print(f'🗑 Canal removido: {before.channel.name}')
            except Exception as error:
                print(f'❌ Erro ao deletar canal: {error}')

# Execução segura do bot
try:
    print('🔄 Iniciando bot...')
    bot.run(TOKEN)
except discord.LoginFailure:
    print('🔒 ERRO: Falha no login - Token inválido!')
except discord.PrivilegedIntentsRequired:
    print('🚨 ERRO: Intents privilegiados não ativados!')
    print('Siga o Passo 1 nas instruções para ativar no portal do Discord')
except Exception as error:
    print(f'🚨 ERRO inesperado: {type(error).__name__}: {error}')