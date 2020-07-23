#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines constants used by autosub.
"""
# Import built-in modules
import os
import re
import sys
import shlex
import locale
import multiprocessing
# from pkg_resources import DistributionNotFound

# Import third-party modules
try:
    from google.cloud.speech_v1p1beta1 import enums  # pylint: disable=unused-import
    IS_GOOGLECLOUDCLIENT = True
except Exception:
    IS_GOOGLECLOUDCLIENT = False
# except DistributionNotFound:
#     IS_GOOGLECLOUDCLIENT = False

from send2trash import send2trash

try:
    import langcodes as langcodes_  # pylint: disable=unused-import
except ImportError:
    langcodes_ = None

# Any changes to the path and your own modules

SUPPORTED_LOCALE = {
    "en_US",
    "zh_CN"
}
# Ref: https://www.gnu.org/software/gettext/manual/html_node/Locale-Names.html#Locale-Names

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable executable'.
    APP_PATH = os.path.dirname(sys.executable)
else:
    APP_PATH = os.path.dirname(__file__)

if sys.platform.startswith('win'):
    DEFAULT_ENCODING = "utf-8-sig"
    IS_UNIX = False
    DELETE_PATH = send2trash
else:
    DEFAULT_ENCODING = "utf-8"
    IS_UNIX = True
    DELETE_PATH = os.remove

LOCALE_PATH = os.path.abspath(os.path.join(APP_PATH, "data/locale"))

EXT_LOCALE = os.path.abspath(os.path.join(os.getcwd(), "locale"))
if os.path.isfile(EXT_LOCALE):
    with open(EXT_LOCALE, encoding='utf-8') as in_file:
        LINE = in_file.readline()
        LINE_LIST = LINE.split()
        if LINE_LIST[0] in SUPPORTED_LOCALE:
            CURRENT_LOCALE = LINE_LIST[0]
        else:
            CURRENT_LOCALE = locale.getdefaultlocale()[0]
else:
    CURRENT_LOCALE = locale.getdefaultlocale()[0]

GOOGLE_SPEECH_V2_API_KEY = "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
GOOGLE_SPEECH_V2_API_URL = \
    "www.google.com/speech-api/v2/recognize?client=chromium&lang={lang}&key={key}"
XFYUN_SPEECH_WEBAPI_URL = "iat-api.xfyun.cn"
BAIDU_ASR_URL = "http://vop.baidu.com/server_api"
BAIDU_PRO_ASR_URL = "http://vop.baidu.com/pro_api"
BAIDU_TOKEN_URL = "http://openapi.baidu.com/oauth/2.0/token"

if multiprocessing.cpu_count() > 3:
    DEFAULT_CONCURRENCY = multiprocessing.cpu_count() >> 1
else:
    DEFAULT_CONCURRENCY = 2

VTT_TIMESTAMP = re.compile(r'\s*((?:\d+:)?\d{2}:\d{2}.\d{3})\s*-->\s*((?:\d+:)?\d{2}:\d{2}.\d{3})')
VTT_WORD_TIMESTAMP = re.compile(r'<(\d{1,2}):(\d{2}):(\d{2})[.,](\d{2,3})>')

DEFAULT_SRC_LANGUAGE = 'en-US'
DEFAULT_ENERGY_THRESHOLD = 50
DEFAULT_MAX_REGION_SIZE = 10.0
DEFAULT_MIN_REGION_SIZE = 0.5
MIN_REGION_SIZE_LIMIT = 0.3
MAX_REGION_SIZE_LIMIT = 60.0
DEFAULT_CONTINUOUS_SILENCE = 0.2
# Maximum speech to text region length in milliseconds
# when using external speech region control

DEFAULT_DST_LANGUAGE = 'en-US'
DEFAULT_SIZE_PER_TRANS = 4000
DEFAULT_SLEEP_SECONDS = 1

DEFAULT_MAX_SIZE_PER_EVENT = 110
DEFAULT_EVENT_DELIMITERS = r"!()*,.:;?[]^_`~"

DEFAULT_SUBTITLES_FORMAT = 'srt'

DEFAULT_MODE_SET = \
    {'regions', 'src', 'full-src', 'dst', 'bilingual', 'dst-lf-src', 'src-lf-dst'}
DEFAULT_SUB_MODE_SET = {'dst', 'bilingual', 'dst-lf-src', 'src-lf-dst'}
DEFAULT_LANG_MODE_SET = {'s', 'src', 'd'}
DEFAULT_AUDIO_PRCS_MODE_SET = {'o', 's', 'y'}

SPEECH_TO_TEXT_LANGUAGE_CODES = {
    'af-za': 'Afrikaans (South Africa)',
    'am-et': 'Amharic (Ethiopia)',
    'ar-ae': 'Arabic (United Arab Emirates)',
    'ar-bh': 'Arabic (Bahrain)',
    'ar-dz': 'Arabic (Algeria)',
    'ar-eg': 'Arabic (Egypt)',
    'ar-il': 'Arabic (Israel)',
    'ar-iq': 'Arabic (Iraq)',
    'ar-jo': 'Arabic (Jordan)',
    'ar-kw': 'Arabic (Kuwait)',
    'ar-lb': 'Arabic (Lebanon)',
    'ar-ma': 'Arabic (Morocco)',
    'ar-om': 'Arabic (Oman)',
    'ar-ps': 'Arabic (State of Palestine)',
    'ar-qa': 'Arabic (Qatar)',
    'ar-sa': 'Arabic (Saudi Arabia)',
    'ar-tn': 'Arabic (Tunisia)',
    'az-az': 'Azerbaijani (Azerbaijan)',
    'bg-bg': 'Bulgarian (Bulgaria)',
    'bn-bd': 'Bengali (Bangladesh)',
    'bn-in': 'Bengali (India)',
    'ca-es': 'Catalan (Spain)',
    'cmn-hans-cn': 'Chinese, Mandarin (Simplified, China)',
    'cmn-hans-hk': 'Chinese, Mandarin (Simplified, Hong Kong)',
    'cmn-hant-tw': 'Chinese, Mandarin (Traditional, Taiwan)',
    'cs-cz': 'Czech (Czech Republic)',
    'da-dk': 'Danish (Denmark)',
    'de-de': 'German (Germany)',
    'el-gr': 'Greek (Greece)',
    'en-au': 'English (Australia)',
    'en-ca': 'English (Canada)',
    'en-gb': 'English (United Kingdom)',
    'en-gh': 'English (Ghana)',
    'en-ie': 'English (Ireland)',
    'en-in': 'English (India)',
    'en-ke': 'English (Kenya)',
    'en-ng': 'English (Nigeria)',
    'en-nz': 'English (New Zealand)',
    'en-ph': 'English (Philippines)',
    'en-sg': 'English (Singapore)',
    'en-tz': 'English (Tanzania)',
    'en-us': 'English (United States)',
    'en-za': 'English (South Africa)',
    'es-ar': 'Spanish (Argentina)',
    'es-bo': 'Spanish (Bolivia)',
    'es-cl': 'Spanish (Chile)',
    'es-co': 'Spanish (Colombia)',
    'es-cr': 'Spanish (Costa Rica)',
    'es-do': 'Spanish (Dominican Republic)',
    'es-ec': 'Spanish (Ecuador)',
    'es-es': 'Spanish (Spain)',
    'es-gt': 'Spanish (Guatemala)',
    'es-hn': 'Spanish (Honduras)',
    'es-mx': 'Spanish (Mexico)',
    'es-ni': 'Spanish (Nicaragua)',
    'es-pa': 'Spanish (Panama)',
    'es-pe': 'Spanish (Peru)',
    'es-pr': 'Spanish (Puerto Rico)',
    'es-py': 'Spanish (Paraguay)',
    'es-sv': 'Spanish (El Salvador)',
    'es-us': 'Spanish (United States)',
    'es-uy': 'Spanish (Uruguay)',
    'es-ve': 'Spanish (Venezuela)',
    'eu-es': 'Basque (Spain)',
    'fa-ir': 'Persian (Iran)',
    'fi-fi': 'Finnish (Finland)',
    'fil-ph': 'Filipino (Philippines)',
    'fr-ca': 'French (Canada)',
    'fr-fr': 'French (France)',
    'gl-es': 'Galician (Spain)',
    'gu-in': 'Gujarati (India)',
    'he-il': 'Hebrew (Israel)',
    'hi-in': 'Hindi (India)',
    'hr-hr': 'Croatian (Croatia)',
    'hu-hu': 'Hungarian (Hungary)',
    'hy-am': 'Armenian (Armenia)',
    'id-id': 'Indonesian (Indonesia)',
    'is-is': 'Icelandic (Iceland)',
    'it-it': 'Italian (Italy)',
    'ja-jp': 'Japanese (Japan)',
    'jv-id': 'Javanese (Indonesia)',
    'ka-ge': 'Georgian (Georgia)',
    'km-kh': 'Khmer (Cambodia)',
    'kn-in': 'Kannada (India)',
    'ko-kr': 'Korean (South Korea)',
    'lo-la': 'Lao (Laos)',
    'lt-lt': 'Lithuanian (Lithuania)',
    'lv-lv': 'Latvian (Latvia)',
    'ml-in': 'Malayalam (India)',
    'mr-in': 'Marathi (India)',
    'ms-my': 'Malay (Malaysia)',
    'nb-no': 'Norwegian Bokmal (Norway)',
    'ne-np': 'Nepali (Nepal)',
    'nl-nl': 'Dutch (Netherlands)',
    'pl-pl': 'Polish (Poland)',
    'pt-br': 'Portuguese (Brazil)',
    'pt-pt': 'Portuguese (Portugal)',
    'ro-ro': 'Romanian (Romania)',
    'ru-ru': 'Russian (Russia)',
    'si-lk': 'Sinhala (Sri Lanka)',
    'sk-sk': 'Slovak (Slovakia)',
    'sl-si': 'Slovenian (Slovenia)',
    'sr-rs': 'Serbian (Serbia)',
    'su-id': 'Sundanese (Indonesia)',
    'sv-se': 'Swedish (Sweden)',
    'sw-ke': 'Swahili (Kenya)',
    'sw-tz': 'Swahili (Tanzania)',
    'ta-in': 'Tamil (India)',
    'ta-lk': 'Tamil (Sri Lanka)',
    'ta-my': 'Tamil (Malaysia)',
    'ta-sg': 'Tamil (Singapore)',
    'te-in': 'Telugu (India)',
    'th-th': 'Thai (Thailand)',
    'tr-tr': 'Turkish (Turkey)',
    'uk-ua': 'Ukrainian (Ukraine)',
    'ur-in': 'Urdu (India)',
    'ur-pk': 'Urdu (Pakistan)',
    'vi-vn': 'Vietnamese (Vietnam)',
    'yue-hant-hk': 'Chinese, Cantonese (Traditional, Hong Kong)',
    'zu-za': 'Zulu (South Africa)'
}

OUTPUT_FORMAT = {
    'srt': 'SubRip',
    'ass': 'Advanced SubStation Alpha',
    'ssa': 'SubStation Alpha',
    'sub': 'MicroDVD Subtitle',
    'mpl2.txt': 'Similar to MicroDVD',
    'tmp': 'TMP Player Subtitle Format',
    'vtt': 'WebVTT',
    'json': 'json(Only times and text)',
    'ass.json': 'json(Complex ass content json)',
    'txt': 'Plain Text(Text or times)'
}

INPUT_FORMAT = {
    'vtt': 'WebVTT',
    'srt': 'SubRip',
    'ass': 'Advanced SubStation Alpha',
    'ssa': 'SubStation Alpha',
    'sub': 'MicroDVD Subtitle',
    'txt': 'Similar to MicroDVD(mpl2)',
    'tmp': 'TMP Player Subtitle Format',
    'json': 'json(Complex ass content json)'
}


def cmd_conversion(command):
    """
    Give a command and return a cross-platform command
    """
    if not IS_UNIX:
        cmd_args = command
    else:
        cmd_args = shlex.split(command)
    return cmd_args


def is_exe(file_path):
    """
    Checks whether a file is executable.
    """
    return os.path.isfile(file_path) and os.access(file_path, os.X_OK)


def which_exe(program_path):
    """
    Return the path for a given executable.
    """
    program_dir = os.path.split(program_path)[0]
    if program_dir:
        # if program directory exists
        if is_exe(program_path):
            return program_path
    else:
        # else find the program path
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            program_name = os.path.join(path, program_path)
            if is_exe(program_name):
                return program_name
        # if program located at app's directory
        program_name = os.path.join(APP_PATH, os.path.basename(program_path))
        if is_exe(program_name):
            return program_name
        # if program located at current directory
        program_name = os.path.join(os.getcwd(), os.path.basename(program_path))
        if is_exe(program_name):
            return program_name
    return None


def get_cmd(program_name):
    """
    Return the path for a given executable.
    "" returned when no executable exists.
    """
    if IS_UNIX:
        command = which_exe(program_name)
        if command:
            return command
    else:
        command = which_exe(program_name + ".exe")
        if command:
            return command

    return ""


def get_cmd_from_env(program_name, env_name):
    """
    Return the path or the value of environment variable
    for a given executable.
    """
    if env_name in os.environ:
        if is_exe(os.environ[env_name]):
            return os.environ[env_name]
        program_name = os.path.join(os.environ[env_name], program_name)
        if is_exe(program_name):
            return program_name
        return program_name + ".exe"
    return get_cmd(program_name)


FFMPEG_CMD = get_cmd_from_env("ffmpeg", "FFMPEG_PATH")
FFPROBE_CMD = get_cmd_from_env("ffprobe", "FFPROBE_PATH")
FFMPEG_NORMALIZE_CMD = get_cmd_from_env("ffmpeg-normalize", "FFMPEG_NORMALIZE_PATH")

DEFAULT_AUDIO_PRCS_CMDS = [
    FFMPEG_CMD + " -hide_banner -i \"{in_}\" -vn -af \"asplit[a],aphasemeter=video=0,\
ametadata=select:key=\
lavfi.aphasemeter.phase:value=-0.005:function=less,\
pan=1c|c0=c0,aresample=async=1:first_pts=0,[a]amix\" \
-ac 1 -f flac -loglevel error \"{out_}\"",
    FFMPEG_CMD + " -hide_banner -i \"{in_}\" -af \"lowpass=3000,highpass=200\" "
                 "-loglevel error \"{out_}\"",
    FFMPEG_NORMALIZE_CMD + " -v \"{in_}\" -ar 44100 -ofmt flac -c:a flac -pr -p -o \"{out_}\""
]

DEFAULT_AUDIO_CVT_CMD = \
    FFMPEG_CMD + " -hide_banner -y -i \"{in_}\" -vn -ac {channel} -ar {sample_rate}" \
                 " -loglevel error \"{out_}\""

DEFAULT_AUDIO_SPLT_CMD = \
    FFMPEG_CMD + " -y -ss {start} -i \"{in_}\" -t {dura} " \
    "-vn -ac [channel] -ar [sample_rate] -loglevel error \"{out_}\""

DEFAULT_VIDEO_FPS_CMD = FFPROBE_CMD + " -v 0 -of csv=p=0 -select_streams " \
                        "v:0 -show_entries stream=r_frame_rate \"{in_}\""

DEFAULT_CHECK_CMD = FFPROBE_CMD + " \"{in_}\" -show_format -pretty -loglevel quiet"

DEFAULT_ENGLISH_STOP_WORDS_SET_1 = \
    {'after', 'and', 'as', 'because', 'before', 'between', 'but', 'either', 'except', 'for', 'how',
     'include', 'including', 'includes', 'included', 'if', 'or', 'since', 'so', 'that', "that'll",
     'until', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'with'}

DEFAULT_ENGLISH_STOP_WORDS_SET_2 = \
    {'a', 'about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an', 'and', 'any',
     'are', 'aren', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below',
     'between', 'both', 'but', 'by', 'can', 'couldn', "couldn't", 'd', 'did', 'didn', "didn't",
     'do', 'does', 'doesn', "doesn't", 'doing', 'don', "don't", 'down', 'during', 'each', 'few',
     'for', 'from', 'further', 'had', 'hadn', "hadn't", 'has', 'hasn', "hasn't", 'have', 'haven',
     "haven't", 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how',
     'i', 'if', 'in', 'into', 'is', 'isn', "isn't", 'it', "it's", 'its', 'itself', 'just', 'll',
     'm', 'ma', 'me', 'mightn', "mightn't", 'more', 'most', 'mustn', "mustn't", 'my', 'myself',
     'needn', "needn't", 'no', 'nor', 'not', 'now', 'o', 'of', 'off', 'on', 'once', 'only', 'or',
     'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 're', 's', 'same', 'shan', "shan't",
     'she', "she's", 'should', "should've", 'shouldn', "shouldn't", 'so', 'some', 'such', 't',
     'than', 'that', "that'll", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there',
     'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 've', 'very',
     'was', 'wasn', "wasn't", 'we', 'were', 'weren', "weren't", 'what', 'when', 'where', 'which',
     'while', 'who', 'whom', 'why', 'will', 'with', 'won', "won't", 'wouldn', "wouldn't", 'y',
     'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'
     }
# Reference: https://gist.github.com/sebleier/554280
