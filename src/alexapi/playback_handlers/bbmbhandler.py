
from __future__ import division
import threading
import logging
import vlc
import re
import RPi.GPIO as GPIO
from threading import Thread
from .vlchandler import VlcHandler, PlaybackAudioType
from pydub import AudioSegment
from time import sleep

logger = logging.getLogger(__name__)
resolution = 20 # fractions / sec

class BbmbHandler(VlcHandler):

    def on_play(self, item):
        logger.info("item url is " + item.url)

        path = False

        # ---------------------------------------------------------------------
        # process audio, local files only
        if re.match(r'^file:///', item.url):
            path = item.url.replace('file://', '')

        elif re.match(r'^/', item.url):
            path = item.url

        if path:
            logger.info("path is " + path)

            sound = AudioSegment.from_mp3(path)

            frames = sound.frame_count()
            frame_rate = sound.frame_rate

            logger.info("sound contains " + str(frames) + " frames at a rate of " + str(frame_rate))

            # -----------------------------------------------------------------
            # process the file 

            segment_size = frame_rate // resolution # 100ms resolution should do it
            i = 0
            levels = []

            while i < frames:

                sample = sound.get_sample_slice(i, i+segment_size)
                i = i + segment_size

                level = sample.rms
                levels.append(level)


            t = Thread(target=self.animate, args=(levels))
            t.start()

        return super (BbmbHandler, self).on_play(item)

    def animate(self, *levels):

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(27, GPIO.OUT)

        # ---------------------------------------
        sleep_period = 1/resolution
        logger.info("sleep period is " + str(sleep_period))

        for level in levels:
            if level > 1000:
                GPIO.output(27, GPIO.HIGH)
            else:
                GPIO.output(27, GPIO.LOW)

            sleep(sleep_period)

            logger.info("level is " + str(level));


