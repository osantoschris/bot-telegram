from pydub import AudioSegment
import os, warnings

warnings.filterwarnings('ignore')

audio_file = r"E:\11. Projetos\12 - Telegram Bot\v2\meu-bot\media\oi_rafael.mp3"

audio = AudioSegment.from_mp3(audio_file)