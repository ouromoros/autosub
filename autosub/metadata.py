#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines autosub's metadata.
"""

_ = str
# For gettext po files

NAME = 'autosub'
VERSION = '0.5.7-alpha'
DESCRIPTION = _('Auto-generate subtitles for video/audio/subtitles file.')
LONG_DESCRIPTION = (
    _('Autosub is an automatic subtitles generating utility. '
      'It can detect speech regions automatically '
      'by using Auditok, split the audio files according to regions '
      'by using ffmpeg, '
      'transcribe speech based on several speech APIs and '
      'translate the subtitles\' text by using py-googletrans.'))
AUTHOR = 'ouromoros'
AUTHOR_EMAIL = 'ouromoros@gmail.com'
HOMEPAGE = 'https://github.com/ouromoros/autosub'
