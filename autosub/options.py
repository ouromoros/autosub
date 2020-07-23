#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines autosub's command line options.
"""
# Import built-in modules
from __future__ import absolute_import, print_function, unicode_literals
import argparse
import gettext

# Import third-party modules
from googletrans import constants as gt_constants

# Any changes to the path and your own modules
from autosub import metadata
from autosub import constants

OPTIONS_TEXT = gettext.translation(domain=__name__,
                                   localedir=constants.LOCALE_PATH,
                                   languages=[constants.CURRENT_LOCALE],
                                   fallback=True)

META_TEXT = gettext.translation(domain=metadata.__name__,
                                localedir=constants.LOCALE_PATH,
                                languages=[constants.CURRENT_LOCALE],
                                fallback=True)

_ = OPTIONS_TEXT.gettext
M_ = META_TEXT.gettext


def get_cmd_parser():  # pylint: disable=too-many-statements
    """
    Get command-line parser.
    """

    parser = argparse.ArgumentParser(
        prog=metadata.NAME,
        usage=_('\n  %(prog)s [-i path] [options]'),
        description=M_(metadata.DESCRIPTION),
        epilog=_("Make sure the argument with space is in quotes.\n"
                 "The default value is used\n"
                 "when the option is not given at the command line.\n"
                 "\"(arg_num)\" means if the option is given,\n"
                 "the number of the arguments is required.\n"
                 "Arguments *ARE* the things given behind the options.\n"
                 "Author: {author}\n"
                 "Email: {email}\n"
                 "Bug report: {homepage}\n").format(
                     author=metadata.AUTHOR,
                     email=metadata.AUTHOR_EMAIL,
                     homepage=metadata.HOMEPAGE),
        add_help=False,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    input_group = parser.add_argument_group(
        _('Input Options'),
        _('Options to control input.'))
    lang_group = parser.add_argument_group(
        _('Language Options'),
        _('Options to control language.'))
    output_group = parser.add_argument_group(
        _('Output Options'),
        _('Options to control output.'))
    speech_group = parser.add_argument_group(
        _('Speech Options'),
        _('Options to control speech-to-text. '
          'If Speech Options not given, it will only generate the times.'))
    trans_group = parser.add_argument_group(
        _('Translation Options'),
        _('Options to control translation.'))
    conversion_group = parser.add_argument_group(
        _('Subtitles Conversion Options'),
        _('Options to control subtitles conversions.(Experimental)'))
    network_group = parser.add_argument_group(
        _('Network Options'),
        _('Options to control network.'))
    options_group = parser.add_argument_group(
        _('Other Options'),
        _('Other options to control.'))
    audio_prcs_group = parser.add_argument_group(
        _('Audio Processing Options'),
        _('Options to control audio processing.'))
    auditok_group = parser.add_argument_group(
        _('Auditok Options'),
        _('Options to control Auditok '
          'when not using external speech regions control.'))
    list_group = parser.add_argument_group(
        _('List Options'),
        _('List all available arguments.'))

    input_group.add_argument(
        '-i', '--input',
        metavar=_('path'),
        help=_("The path to the video/audio/subtitles file "
               "that needs to generate subtitles. "
               "When it is a subtitles file, "
               "the program will only translate it. "
               "(arg_num = 1)"))

    input_group.add_argument(
        '-er', '--ext-regions',
        metavar=_('path'),
        help=_("Path to the subtitles file "
               "which provides external speech regions, "
               "which is one of the formats that pysubs2 supports "
               "and overrides the default method to find speech regions. "
               "(arg_num = 1)"))

    input_group.add_argument(
        '-sty', '--styles',
        nargs='?', metavar=_('path'),
        const=' ',
        help=_("Valid when your output format is \"ass\"/\"ssa\". "
               "Path to the subtitles file "
               "which provides \"ass\"/\"ssa\" styles for your output. "
               "If the arg_num is 0, "
               "it will use the styles from the : "
               "\"-er\"/\"--external-speech-regions\". "
               "More info on \"-sn\"/\"--styles-name\". "
               "(arg_num = 0 or 1)"))

    input_group.add_argument(
        '-sn', '--style-name',
        nargs='*', metavar=_('style_name'),
        help=_("Valid when your output format is \"ass\"/\"ssa\" "
               "and \"-sty\"/\"--styles\" is given. "
               "Adds \"ass\"/\"ssa\" styles to your events. "
               "If not provided, events will use the first one "
               "from the file. "
               "If the arg_num is 1, events will use the "
               "specific style from the arg of \"-sty\"/\"--styles\". "
               "If the arg_num is 2, src language events use the first. "
               "Dst language events use the second. "
               "(arg_num = 1 or 2)"))

    lang_group.add_argument(
        '-S', '--speech-language',
        metavar=_('lang_code'),
        help=_("Lang code/Lang tag for speech-to-text. "
               "Recommend using the Google Cloud Speech reference "
               "lang codes. "
               "WRONG INPUT WON'T STOP RUNNING. "
               "But use it at your own risk. "
               "Ref: https://cloud.google.com/speech-to-text/docs/languages"
               "(arg_num = 1) (default: %(default)s)"))

    lang_group.add_argument(
        '-SRC', '--src-language',
        metavar=_('lang_code'),
        default='auto',
        help=_("Lang code/Lang tag for translation source language. "
               "If not given, use py-googletrans to auto-detect the src language. "
               "(arg_num = 1) (default: %(default)s)"))

    lang_group.add_argument(
        '-D', '--dst-language',
        metavar=_('lang_code'),
        help=_("Lang code/Lang tag for translation destination language. "
               "(arg_num = 1) (default: %(default)s)"))

    lang_group.add_argument(
        '-bm', '--best-match',
        metavar=_('mode'),
        nargs="*",
        help=_("Use langcodes to get a best matching lang code "
               "when your input is wrong. "
               "Only functional for py-googletrans and Google Speech API. "
               "If langcodes not installed, use fuzzywuzzy instead. "
               "Available modes: "
               "s, src, d, all. "
               "\"s\" for \"-S\"/\"--speech-language\". "
               "\"src\" for \"-SRC\"/\"--src-language\". "
               "\"d\" for \"-D\"/\"--dst-language\". "
               "(3 >= arg_num >= 1)"))

    lang_group.add_argument(
        '-mns', '--min-score',
        metavar='integer',
        type=int,
        help=_("An integer between 0 and 100 "
               "to control the good match group of "
               "\"-lsc\"/\"--list-speech-codes\" "
               "or \"-ltc\"/\"--list-translation-codes\" "
               "or the match result in \"-bm\"/\"--best-match\". "
               "Result will be a group of \"good match\" "
               "whose score is above this arg. "
               "(arg_num = 1)"))

    output_group.add_argument(
        '-o', '--output',
        metavar=_('path'),
        help=_("The output path for subtitles file. "
               "(default: the \"input\" path combined "
               "with the proper name tails) (arg_num = 1)"))

    output_group.add_argument(
        '-F', '--format',
        metavar=_('format'),
        help=_("Destination subtitles format. "
               "If not provided, use the extension "
               "in the \"-o\"/\"--output\" arg. "
               "If \"-o\"/\"--output\" arg doesn't provide "
               "the extension name, use \"{dft}\" instead. "
               "In this case, if \"-i\"/\"--input\" arg is a subtitles file, "
               "use the same extension from the subtitles file. "
               "(arg_num = 1) (default: {dft})").format(
                   dft=constants.DEFAULT_SUBTITLES_FORMAT))

    output_group.add_argument(
        '-y', '--yes',
        action='store_true',
        help=_("Prevent pauses and allow files to be overwritten. "
               "Stop the program when your args are wrong. (arg_num = 0)"))

    output_group.add_argument(
        '-of', '--output-files',
        metavar=_('type'),
        nargs='*',
        default=["dst", ],
        help=_("Output more files. "
               "Available types: "
               "regions, src, full-src, dst, bilingual, dst-lf-src, src-lf-dst, all. "
               "\"regions\", \"src\", \"full-src\" are available only "
               "if input is not a subtitles file. "
               "full-src: Full result received from Speech-to-Text API in json format "
               "with start and end time. "
               "dst-lf-src: dst language and src language in the same event. "
               "And dst is ahead of src. "
               "src-lf-dst: src language and dst language in the same event. "
               "And src is ahead of dst. "
               "(6 >= arg_num >= 1) (default: %(default)s)"))

    output_group.add_argument(
        '-fps', '--sub-fps',
        metavar='float',
        type=float,
        help=_("Valid when your output format is \"sub\". "
               "If input, it will override the fps check "
               "on the input file. "
               "Ref: https://pysubs2.readthedocs.io/en/latest/api-reference.html"
               "#supported-input-output-formats "
               "(arg_num = 1)"))

    speech_group.add_argument(
        '-sapi', '--speech-api',
        metavar=_('API_code'),
        default='gsv2',
        choices=["gsv2", "gcsv1", "xfyun", "baidu", "deepspeech"],
        help=_("Choose which Speech-to-Text API to use. "
               "Currently support: "
               "gsv2: Google Speech V2 (https://github.com/gillesdemey/google-speech-v2). "
               "gcsv1: Google Cloud Speech-to-Text V1P1Beta1 "
               "(https://cloud.google.com/speech-to-text/docs). "
               "xfyun: Xun Fei Yun Speech-to-Text WebSocket API "
               "(https://www.xfyun.cn/doc/asr/voicedictation/API.html). "
               "baidu: Baidu Automatic Speech Recognition API "
               "(https://ai.baidu.com/ai-doc/SPEECH/Vk38lxily) "
               "(arg_num = 1) (default: %(default)s)"))

    speech_group.add_argument(
        '-skey', '--speech-key',
        metavar='key',
        help=_("The API key for Google Speech-to-Text API. (arg_num = 1) "
               "Currently support: "
               "gsv2: The API key for gsv2. (default: Free API key) "
               "gcsv1: The API key for gcsv1. "
               "(If used, override the credentials "
               "given by\"-sa\"/\"--service-account\")"))

    speech_group.add_argument(
        '-sconf', '--speech-config',
        nargs='?', metavar=_('path'),
        const='config.json',
        help=_("Use Speech-to-Text recognition config file to send request. "
               "Override these options below: "
               "\"-S\", \"-asr\", \"-asf\". "
               "Currently support: "
               "gcsv1: Google Cloud Speech-to-Text V1P1Beta1 "
               "API key config reference: "
               "https://cloud.google.com/speech-to-text/docs"
               "/reference/rest/v1p1beta1/RecognitionConfig "
               "Service account config reference: "
               "https://googleapis.dev/python/speech/latest"
               "/gapic/v1/types.html"
               "#google.cloud.speech_v1.types.RecognitionConfig "
               "xfyun: Xun Fei Yun Speech-to-Text WebSocket API "
               "(https://console.xfyun.cn/services/iat). "
               "baidu: Baidu Automatic Speech Recognition API "
               "(https://ai.baidu.com/ai-doc/SPEECH/ek38lxj1u). "
               "If arg_num is 0, use const path. "
               "(arg_num = 0 or 1) (const: %(const)s)")
    )

    speech_group.add_argument(
        '-mnc', '--min-confidence',
        metavar='float',
        type=float,
        default=0.0,
        help=_("Google Speech-to-Text API response for text confidence. "
               "A float value between 0 and 1. "
               "Confidence bigger means the result is better. "
               "Input this argument will drop any result below it. "
               "Ref: https://github.com/BingLingGroup/google-speech-v2#response "
               "(arg_num = 1) (default: %(default)s)"))

    speech_group.add_argument(
        '-der', '--drop-empty-regions',
        action='store_true',
        help=_("Drop any regions without speech recognition result. "
               "(arg_num = 0)"))

    speech_group.add_argument(
        '-sc', '--speech-concurrency',
        metavar='integer',
        type=int,
        default=constants.DEFAULT_CONCURRENCY,
        help=_("Number of concurrent Speech-to-Text requests to make. "
               "(arg_num = 1) (default: %(default)s)"))

    trans_group.add_argument(
        '-tapi', '--translation-api',
        metavar=_('API_code'),
        default='pygt',
        choices=["pygt", "man"],
        help=_("Choose which translation API to use. "
               "Currently support: "
               "pygt: py-googletrans (https://py-googletrans.readthedocs.io/en/latest/). "
               "man: Manually translate the content by write a txt or docx file and then read it. "
               "(arg_num = 1) (default: %(default)s)"))

    trans_group.add_argument(
        '-tf', '--translation-format',
        metavar=_('format'),
        default='docx',
        choices=["docx", "txt"],
        help=_("Choose which output format for manual translation to use. "
               "Currently support: docx, txt. "
               "(arg_num = 1) (default: %(default)s)"))

    trans_group.add_argument(
        '-mts', '--max-trans-size',
        metavar='integer',
        type=int,
        default=constants.DEFAULT_SIZE_PER_TRANS,
        help=_("(Experimental)Max size per translation request. "
               "(arg_num = 1) (default: %(default)s)"))

    trans_group.add_argument(
        '-slp', '--sleep-seconds',
        metavar=_('second'),
        type=float,
        default=constants.DEFAULT_SLEEP_SECONDS,
        help=_("(Experimental)Seconds for py-googletrans to sleep "
               "between two translation requests. "
               "(arg_num = 1) (default: %(default)s)"))

    trans_group.add_argument(
        '-surl', '--service-urls',
        metavar='URL',
        default=["translate.google.com"],
        nargs='*',
        help=_("(Experimental)Customize py-googletrans request urls. "
               "Ref: https://py-googletrans.readthedocs.io/en/latest/ "
               "(arg_num >= 1)"))

    trans_group.add_argument(
        '-ua', '--user-agent',
        metavar='User-Agent headers',
        default=gt_constants.DEFAULT_USER_AGENT,
        help=_("(Experimental)Customize py-googletrans User-Agent headers. "
               "Same docs above. "
               "(arg_num = 1)"))

    trans_group.add_argument(
        '-doc', '--drop-override-codes',
        action='store_true',
        help=_("Drop any .ass override codes in the text before translation. "
               "Only affect the translation result. "
               "(arg_num = 0)"))

    trans_group.add_argument(
        '-tdc', '--trans-delete-chars',
        nargs='?', metavar="chars",
        const="，。！",
        help=_("Replace the specific chars with a space after translation, "
               "and strip the space at the end of each sentence. "
               "Only affect the translation result. "
               "(arg_num = 0 or 1) (const: %(const)s)"))

    conversion_group.add_argument(
        '-mjs', '--max-join-size',
        metavar='integer',
        type=int,
        default=constants.DEFAULT_MAX_SIZE_PER_EVENT,
        help=_("(Experimental)Max length to join two events. "
               "(arg_num = 1) (default: %(default)s)"))

    conversion_group.add_argument(
        '-mdt', '--max-delta-time',
        metavar=_('second'),
        type=float,
        default=constants.DEFAULT_CONTINUOUS_SILENCE,
        help=_("(Experimental)Max delta time to join two events. "
               "(arg_num = 1) (default: %(default)s)"))

    conversion_group.add_argument(
        '-dms', '--delimiters',
        metavar=_('string'),
        default=constants.DEFAULT_EVENT_DELIMITERS,
        help=_("(Experimental)Delimiters not to join two events. "
               "(arg_num = 1) (default: %(default)s)"))

    conversion_group.add_argument(
        '-sw1', '--stop-words-1',
        metavar=_('words_delimited_by_space'),
        help=_("(Experimental)First set of Stop words to split two events. "
               "(arg_num = 1)"))

    conversion_group.add_argument(
        '-sw2', '--stop-words-2',
        metavar=_('words_delimited_by_space'),
        help=_("(Experimental)Second set of Stop words to split two events. "
               "(arg_num = 1)"))

    conversion_group.add_argument(
        '-ds', '--dont-split',
        action='store_true',
        help=_("(Experimental)Don't split. Just merge. "
               "(arg_num = 0)"))

    conversion_group.add_argument(
        '-jctl', '--join-control',
        metavar=_('string'),
        nargs='*',
        help=_("Control the way to join events when using vtt. "
               "Key tag choice: [\"\\k\", \"\\ko\", \"\\kf\", (None)] (default: None). "
               "Events manual adjustment: [\"man\", \"semi-auto\", \"auto\"] (default: man). "
               "Auto capitalization and full stop: [\"cap\", (None)] (default: None). "
               "Trim regions after processing: [\"trim\", (None)] (default: None). "
               "(arg_num >= 1)"))

    network_group.add_argument(
        '-hsa', '--http-speech-api',
        action='store_true',
        help=_("Change the Google Speech V2 API "
               "URL into the http one. "
               "(arg_num = 0)"))

    network_group.add_argument(
        '-hsp', '--https-proxy',
        nargs='?', metavar='URL',
        const='https://127.0.0.1:1080',
        help=_("Add https proxy by setting environment variables. "
               "If arg_num is 0, use const proxy url. "
               "(arg_num = 0 or 1) (const: %(const)s)"))

    network_group.add_argument(
        '-hp', '--http-proxy',
        nargs='?', metavar='URL',
        const='http://127.0.0.1:1080',
        help=_("Add http proxy by setting environment variables. "
               "If arg_num is 0, use const proxy url. "
               "(arg_num = 0 or 1) (const: %(const)s)"))

    network_group.add_argument(
        '-pu', '--proxy-username',
        metavar=_('username'),
        help=_("Set proxy username. "
               "(arg_num = 1)"))

    network_group.add_argument(
        '-pp', '--proxy-password',
        metavar=_('password'),
        help=_("Set proxy password. "
               "(arg_num = 1)"))

    options_group.add_argument(
        '-h', '--help',
        action='help',
        help=_("Show %(prog)s help message and exit. (arg_num = 0)"))

    options_group.add_argument(
        '-V', '--version',
        action='version',
        version='%(prog)s ' + metadata.VERSION
        + ' by ' + metadata.AUTHOR + ' <'
        + metadata.AUTHOR_EMAIL + '>',
        help=_("Show %(prog)s version and exit. (arg_num = 0)"))

    options_group.add_argument(
        '-sa', '--service-account',
        metavar=_('path'),
        help=_("Set service account key environment variable. "
               "It should be the file path of the JSON file "
               "that contains your service account credentials. "
               "Can be overridden by the API key. "
               "Ref: https://cloud.google.com/docs/authentication/getting-started "
               "Currently support: gcsv1 (GOOGLE_APPLICATION_CREDENTIALS) "
               "(arg_num = 1)"))

    audio_prcs_group.add_argument(
        '-ap', '--audio-process',
        nargs='*', metavar=_('mode'),
        help=_("Option to control audio process. "
               "If not given the option, "
               "do normal conversion work. "
               "\"y\": pre-process the input first "
               "then start normal workflow. "
               "If succeed, no more conversion before "
               "the speech-to-text procedure. "
               "\"o\": only pre-process the input audio. "
               "(\"-k\"/\"--keep\" is true) "
               "\"s\": only split the input audio. "
               "(\"-k\"/\"--keep\" is true) "
               "Default command to pre-process the audio: "
               "{dft_1} | {dft_2} | {dft_3} "
               "(Ref: "
               "https://github.com/stevenj/autosub/blob/master/scripts/subgen.sh "
               "https://ffmpeg.org/ffmpeg-filters.html) "
               "(2 >= arg_num >= 1)").format(
                   dft_1=constants.DEFAULT_AUDIO_PRCS_CMDS[0],
                   dft_2=constants.DEFAULT_AUDIO_PRCS_CMDS[1],
                   dft_3=constants.DEFAULT_AUDIO_PRCS_CMDS[2]))

    audio_prcs_group.add_argument(
        '-k', '--keep',
        action='store_true',
        help=_("Keep audio processing files to the output path. "
               "(arg_num = 0)"))

    audio_prcs_group.add_argument(
        '-apc', '--audio-process-cmd',
        nargs='*', metavar=_('command'),
        help=_("This arg will override the default "
               "audio pre-process command. "
               "Every line of the commands need to be in quotes. "
               "Input file name is {in_}. "
               "Output file name is {out_}. "
               "(arg_num >= 1)"))

    audio_prcs_group.add_argument(
        '-ac', '--audio-concurrency',
        metavar='integer',
        type=int,
        default=constants.DEFAULT_CONCURRENCY,
        help=_("Number of concurrent ffmpeg audio split process to make. "
               "(arg_num = 1) (default: %(default)s)"))

    audio_prcs_group.add_argument(
        '-acc', '--audio-conversion-cmd',
        metavar=_('command'),
        default=constants.DEFAULT_AUDIO_CVT_CMD,
        help=_("(Experimental)This arg will override the default "
               "audio conversion command. "
               "\"[\", \"]\" are optional arguments "
               "meaning you can remove them. "
               "\"{\", \"}\" are required arguments "
               "meaning you can't remove them. "
               "(arg_num = 1) (default: %(default)s)"))

    audio_prcs_group.add_argument(
        '-asc', '--audio-split-cmd',
        metavar=_('command'),
        default=constants.DEFAULT_AUDIO_SPLT_CMD,
        help=_("(Experimental)This arg will override the default "
               "audio split command. "
               "Same attention above. "
               "(arg_num = 1) (default: %(default)s)"))

    audio_prcs_group.add_argument(
        '-asf', '--api-suffix',
        metavar=_('file_suffix'),
        default='.flac',
        help=_("(Experimental)This arg will override the default "
               "API audio suffix. "
               "(arg_num = 1) (default: %(default)s)"))

    audio_prcs_group.add_argument(
        '-asr', '--api-sample-rate',
        metavar=_('sample_rate'),
        type=int,
        default=44100,
        help=_("(Experimental)This arg will override the default "
               "API audio sample rate(Hz). "
               "(arg_num = 1) (default: %(default)s)"))

    audio_prcs_group.add_argument(
        '-aac', '--api-audio-channel',
        metavar=_('channel_num'),
        type=int,
        default=1,
        help=_("(Experimental)This arg will override the default "
               "API audio channel. "
               "(arg_num = 1) (default: %(default)s)"))

    auditok_group.add_argument(
        '-et', '--energy-threshold',
        metavar=_('energy'),
        type=int,
        default=constants.DEFAULT_ENERGY_THRESHOLD,
        help=_("The energy level which determines the region to be detected. "
               "Ref: https://auditok.readthedocs.io/en/latest/apitutorial.html"
               "#examples-using-real-audio-data "
               "(arg_num = 1) (default: %(default)s)"))

    auditok_group.add_argument(
        '-mnrs', '--min-region-size',
        metavar=_('second'),
        type=float,
        default=constants.DEFAULT_MIN_REGION_SIZE,
        help=_("Minimum region size. "
               "Same docs above. "
               "(arg_num = 1) (default: %(default)s)"))

    auditok_group.add_argument(
        '-mxrs', '--max-region-size',
        metavar=_('second'),
        type=float,
        default=constants.DEFAULT_MAX_REGION_SIZE,
        help=_("Maximum region size. "
               "Same docs above. "
               "(arg_num = 1) (default: %(default)s)"))

    auditok_group.add_argument(
        '-mxcs', '--max-continuous-silence',
        metavar=_('second'),
        type=float,
        default=constants.DEFAULT_CONTINUOUS_SILENCE,
        help=_("Maximum length of a tolerated silence within a valid audio activity. "
               "Same docs above. "
               "(arg_num = 1) (default: %(default)s)"))

    auditok_group.add_argument(
        '-nsml', '--not-strict-min-length',
        action='store_true',
        help=_("If not input this option, "
               "it will keep all regions strictly follow the minimum region limit. "
               "Ref: https://auditok.readthedocs.io/en/latest/core.html#class-summary "
               "(arg_num = 0)"))

    auditok_group.add_argument(
        '-dts', '--drop-trailing-silence',
        action='store_true',
        help=_("Ref: https://auditok.readthedocs.io/en/latest/core.html#class-summary "
               "(arg_num = 0)"))

    auditok_group.add_argument(
        '-aconf', '--auditok-config',
        nargs='?', metavar=_('path'),
        const='aconfig.json',
        help=_("Auditok options automatic optimization config."
               "(arg_num = 0 or 1)"))

    list_group.add_argument(
        '-lf', '--list-formats',
        action='store_true',
        help=_("List all available subtitles formats. "
               "If your format is not supported, "
               "you can use ffmpeg or SubtitleEdit to convert the formats. "
               "You need to offer fps option "
               "when input is an audio file "
               "and output is \"sub\" format. "
               "(arg_num = 0)"))

    list_group.add_argument(
        '-lsc', '--list-speech-codes',
        metavar=_('lang_code'),
        const=' ',
        nargs='?',
        help=_("List all recommended \"-S\"/\"--speech-language\" "
               "Google Speech-to-Text language codes. "
               "If no arg is given, list all. "
               "Or else will list a group of \"good match\" "
               "of the arg. Default \"good match\" standard is whose "
               "match score above 90 (score between 0 and 100). "
               "Ref: https://tools.ietf.org/html/bcp47 "
               "https://github.com/LuminosoInsight/langcodes/blob/master/langcodes/__init__.py "
               "lang code example: language-script-region-variant-extension-privateuse "
               "(arg_num = 0 or 1)"))

    list_group.add_argument(
        '-ltc', '--list-translation-codes',
        metavar=_('lang_code'),
        const=' ',
        nargs='?',
        help=_("List all available \"-SRC\"/\"--src-language\" "
               "py-googletrans translation language codes. "
               "Or else will list a group of \"good match\" "
               "of the arg. "
               "Same docs above. "
               "(arg_num = 0 or 1)"))

    list_group.add_argument(
        '-dsl', '--detect-sub-language',
        metavar=_('path'),
        help=_("Use py-googletrans to detect a sub file's first line language. "
               "And list a group of matched language in recommended "
               "\"-S\"/\"--speech-language\" Google Speech-to-Text language codes. "
               "Ref: https://cloud.google.com/speech-to-text/docs/languages "
               "(arg_num = 1) (default: %(default)s)"))

    return parser
